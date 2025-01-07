from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_openai import ChatOpenAI
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import AsyncIterator, List, Dict, Any
import json
import logging
import asyncio
from app.core.config import settings
from .tools import get_tools

logger = logging.getLogger(__name__)


class AgentManager:
    def __init__(self):
        self.tools = get_tools()
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
        )

    def _format_tools_for_prompt(self) -> Dict[str, str]:
        """Format tools for the prompt template."""
        tool_strings = []
        tool_names = []
        for tool in self.tools:
            tool_strings.append(f"{tool.name}: {tool.description}")
            tool_names.append(tool.name)

        return {"tools": "\n".join(tool_strings), "tool_names": ", ".join(tool_names)}

    async def analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze if the query needs tools or can be answered directly."""
        analysis_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an AI that analyzes whether queries require external tools or can be answered with general knowledge. "
                    "For queries about current weather, stock prices, or real-time data, always indicate that tools are required.",
                ),
                (
                    "human",
                    "Analyze this query: {query}\n\n"
                    "Respond with a strict JSON object:\n"
                    '{"requires_tools": false, "reasoning": "string", "direct_response": "string"}\n\n'
                    "Note: Use true/false (lowercase) for the requires_tools field.",
                ),
            ]
        )

        messages = analysis_prompt.format_messages(query=query)
        response = await self.llm.ainvoke(messages)
        try:
            # Clean the response content and ensure valid JSON
            cleaned_response = response.content.strip()
            # Convert JavaScript-style booleans to Python-style
            cleaned_response = cleaned_response.replace("true", "True").replace(
                "false", "False"
            )
            return eval(
                cleaned_response
            )  # safer than json.loads() for Python boolean values
        except Exception as e:
            logger.error(f"Failed to parse analysis response: {e}")
            return {
                "requires_tools": True,
                "reasoning": "Failed to analyze query properly",
                "direct_response": None,
            }

    async def get_direct_response(self, query: str) -> str:
        """Get a direct response for queries that don't require tools."""
        messages = [
            SystemMessage(
                content="You are a helpful AI assistant. Provide clear, concise responses based on your knowledge."
            ),
            HumanMessage(content=query),
        ]
        response = await self.llm.ainvoke(messages)
        return response.content

    async def create_agent(self, callback_handler: AsyncIteratorCallbackHandler):
        """Create an agent with properly formatted tool information."""
        llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            streaming=True,
            callbacks=[callback_handler],
        )

        tool_format = self._format_tools_for_prompt()
        prompt_template = f"""You are a helpful AI assistant that can use tools to get information and help users.
        Always think step by step about what tools you need to use to help the user.
        If you don't know something or if a tool fails, please say so.
        
        You have access to the following tools:
        {tool_format['tools']}
        
        To use a tool, please use the following format:
        Action: the action to take, should be one of [{{tool_names}}]
        Action Input: the input to the action
        Observation: the result of the action
        
        When you have a final response to say to the Human, or if you do not need to use a tool, you MUST use the format:
        Final Answer: [your response here]"""

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = create_structured_chat_agent(
            llm=llm, tools=self.tools, prompt=prompt.partial(**tool_format)
        )

        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3,
            early_stopping_method="generate",
        )

    async def process_task(self, task: str) -> AsyncIterator[str]:
        """Process a task, either directly or using tools based on analysis."""
        try:
            # Initial processing message
            yield f"data: {json.dumps({'text': '**Starting request processing...**\n', 'type': 'system'})}\n\n"

            # Analyze query
            yield f"data: {json.dumps({'text': '**Analyzing query...**\n', 'type': 'system'})}\n\n"
            analysis = await self.analyze_query(task)
            yield f"data: {json.dumps({'text': f'Reasoning: {analysis.get("reasoning", "No reasoning provided")}\n', 'type': 'system'})}\n\n"

            if not analysis.get("requires_tools", False):
                # Handle direct response
                yield f"data: {json.dumps({'text': '**Generating direct response...**\n', 'type': 'system'})}\n\n"
                if "direct_response" in analysis:
                    response = analysis["direct_response"]
                else:
                    response = await self.get_direct_response(task)
                yield f"data: {json.dumps({'text': response, 'type': 'agent_final'})}\n\n"
                return

            # Handle tool-based response
            yield f"data: {json.dumps({'text': '**Executing agent tasks...**\n', 'type': 'system'})}\n\n"
            callback = AsyncIteratorCallbackHandler()
            agent_executor = await self.create_agent(callback)

            task_future = asyncio.create_task(
                agent_executor.ainvoke(
                    {"input": task, "chat_history": [], "agent_scratchpad": []}
                )
            )

            current_message = []
            async for token in callback.aiter():
                current_message.append(token)
                message = "".join(current_message)

                if "Action:" in message:
                    yield f"data: {json.dumps({'text': f'\n{message}', 'type': 'agent_action'})}\n\n"
                    current_message = []
                elif "Observation:" in message:
                    yield f"data: {json.dumps({'text': f'\n{message}', 'type': 'agent_observation'})}\n\n"
                    current_message = []
                elif len(token.strip()) > 0:
                    yield f"data: {json.dumps({'text': token, 'type': 'agent_thought'})}\n\n"

            try:
                final_result = await asyncio.wait_for(task_future, timeout=30.0)
                if final_result and "output" in final_result:
                    yield f"data: {json.dumps({'text': f'\nFinal Answer: {final_result['output']}', 'type': 'agent_final'})}\n\n"
            except asyncio.TimeoutError:
                yield f"data: {json.dumps({'text': '\nTask timed out', 'type': 'error'})}\n\n"
            except Exception as e:
                logger.error(f"Error getting final result: {str(e)}")
                yield f"data: {json.dumps({'text': f'\nError in final result: {str(e)}', 'type': 'error'})}\n\n"

        except Exception as e:
            logger.error(f"Error in task processing: {str(e)}")
            yield f"data: {json.dumps({'text': f'Error: {str(e)}', 'type': 'error'})}\n\n"

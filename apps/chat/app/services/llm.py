from langchain_openai import ChatOpenAI
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from typing import AsyncIterator, List, Dict
import asyncio
import json
from app.core.config import settings
import logging
from app.services.agents.manager import AgentManager

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.agent_manager = AgentManager()

        self.system_prompt = """You are an intelligent AI assistant that can both answer questions directly and use specialized tools when needed.

Available Tools and their Capabilities:
1. get_time: Get current time in any timezone
2. get_date: Get current date in any timezone
3. search_docs: Search through documents for specific information
4. analyze_sentiment: Analyze the sentiment of given text
5. web_search: Search the internet for recent or specific information

Before responding, analyze if the question requires real-time data, current information, or specialized tools.
If the question can be answered with your general knowledge, respond directly.
If tools are needed, specify which tool and why.

IMPORTANT: Your response must be valid JSON in the following format:
{
    "requires_tool": true/false,
    "tool_name": "name_of_tool_or_null",
    "reasoning": "your explanation here",
    "direct_response": "your response if no tool is needed or null"
}"""

    async def analyze_query(self, query: str) -> Dict:
        """Analyze the query to determine if tools are needed."""
        llm = ChatOpenAI(
            api_key=self.api_key,
            model=settings.MODEL_NAME,
            temperature=0.2,  # Lower temperature for more consistent decision making
            streaming=False,  # Disable streaming for the analysis
        )

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(
                content=f"Question: {query}\n\nAnalyze this question and decide how to respond."
            ),
        ]

        try:
            response = await llm.ainvoke(messages)
            # Parse the response as JSON
            decision = json.loads(response.content)
            logger.info(f"Query analysis decision: {decision}")
            return decision
        except json.JSONDecodeError as e:
            logger.error(
                f"Error parsing LLM decision JSON: {str(e)}, Response: {response.content}"
            )
            return {
                "requires_tool": False,
                "tool_name": None,
                "reasoning": "Error in analysis, falling back to direct response",
                "direct_response": None,
            }
        except Exception as e:
            logger.error(f"Unexpected error in analyze_query: {str(e)}")
            return {
                "requires_tool": False,
                "tool_name": None,
                "reasoning": f"Unexpected error: {str(e)}",
                "direct_response": None,
            }

    async def generate_stream(
        self, query: str, context: List[str]
    ) -> AsyncIterator[str]:
        try:
            # First, analyze if we need to use tools
            yield f"data: {json.dumps({'text': 'Analyzing query...', 'type': 'system'})}\n\n"

            decision = await self.analyze_query(query)

            yield f"data: {json.dumps({'text': f'\nReasoning: {decision.get("reasoning", "No reasoning provided")}', 'type': 'analysis'})}\n\n"

            if decision.get("requires_tool", False):
                tool_name = decision.get("tool_name")
                if not tool_name:
                    yield f"data: {json.dumps({'text': 'Error: No tool specified', 'type': 'error'})}\n\n"
                    return

                yield f"data: {json.dumps({'text': f'\nUsing tool: {tool_name}', 'type': 'system'})}\n\n"
                # Use the agent manager to handle the tool-based response
                async for chunk in self.agent_manager.process_task(query):
                    yield chunk
            else:
                # Generate direct response
                callback = AsyncIteratorCallbackHandler()
                llm = ChatOpenAI(
                    api_key=self.api_key,
                    model=settings.MODEL_NAME,
                    temperature=settings.TEMPERATURE,
                    streaming=True,
                    callbacks=[callback],
                )

                messages = [
                    SystemMessage(
                        content="You are a helpful AI assistant. Provide accurate and relevant information based on the given context."
                    ),
                    HumanMessage(
                        content=f"Context: {' '.join(context)}\n\nQuestion: {query}"
                    ),
                ]

                task = asyncio.create_task(llm.ainvoke(messages))

                yield f"data: {json.dumps({'text': '\nGenerating response...', 'type': 'system'})}\n\n"

                async for token in callback.aiter():
                    yield f"data: {json.dumps({'text': token, 'type': 'response'})}\n\n"

                await task

        except Exception as e:
            logger.error(
                "Error in stream generation", extra={"props": {"error": str(e)}}
            )
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

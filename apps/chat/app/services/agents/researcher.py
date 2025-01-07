from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from typing import Dict, TypedDict, Annotated
import json


class ResearcherState(TypedDict):
    query: str
    requires_agent: bool
    agent_type: str | None
    context: str | None


class Researcher:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.system_prompt = """You are a research coordinator. Your job is to:
        1. Determine if the query requires an agent to perform actions
        2. If yes, specify which type of agent is needed: 'calculator', 'web_search', or 'code_executor'
        3. If no, specify that only context-based response is needed
        
        Respond in JSON format:
        {
            "requires_agent": boolean,
            "agent_type": string or null,
            "reasoning": string
        }"""

    async def decide(self, state: ResearcherState) -> ResearcherState:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Query: {state['query']}"),
        ]

        response = await self.llm.ainvoke(messages)
        decision = json.loads(response.content)

        return {
            **state,
            "requires_agent": decision["requires_agent"],
            "agent_type": (
                decision["agent_type"] if decision["requires_agent"] else None
            ),
        }

from typing import Dict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import re


class Calculator:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.system_prompt = """You are a calculator agent. Extract numerical values and perform calculations."""

    async def calculate(self, state: Dict) -> Dict:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Calculate this: {state['query']}"),
        ]

        response = await self.llm.ainvoke(messages)
        return {**state, "calculation_result": response.content}

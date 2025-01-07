from langgraph.graph import StateGraph, END
from typing import Annotated, Dict, TypedDict
from app.services.agents.researcher import Researcher, ResearcherState
from app.services.agents.calculator import Calculator
from app.services.llm import LLMService


class WorkflowState(TypedDict):
    query: str
    requires_agent: bool
    agent_type: str | None
    context: str | None
    final_response: str | None


class WorkflowManager:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.researcher = Researcher(llm_service.llm)
        self.calculator = Calculator(llm_service.llm)
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("researcher", self.researcher.decide)
        workflow.add_node("calculator", self.calculator.calculate)
        workflow.add_node("context_response", self.handle_context_response)

        # Add edges
        workflow.add_edge("researcher", self._route_based_on_research)
        workflow.add_edge("calculator", "context_response")
        workflow.add_edge("context_response", END)

        workflow.set_entry_point("researcher")
        return workflow.compile()

    async def handle_context_response(self, state: WorkflowState) -> WorkflowState:
        if state.get("context"):
            response = await self.llm_service.get_response(
                state["query"], state["context"]
            )
            return {**state, "final_response": response["answer"]}
        return state

    def _route_based_on_research(self, state: WorkflowState) -> str:
        if not state["requires_agent"]:
            return "context_response"

        if state["agent_type"] == "calculator":
            return "calculator"

        # Add more agent routing here
        return "context_response"

    async def run_workflow(self, query: str, context: str | None = None) -> Dict:
        initial_state = {
            "query": query,
            "requires_agent": False,
            "agent_type": None,
            "context": context,
            "final_response": None,
        }

        result = await self.workflow.ainvoke(initial_state)
        return result

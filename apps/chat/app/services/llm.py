from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from typing import Dict, List
import logging
from app.core.config import settings
from app.services.workflow import WorkflowManager
import json

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Initialize LLM
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
        )

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_template(
            """
        Answer the following question based only on the provided context:
        <context>
        {context}
        </context>
        Question: {input}
        """
        )

        self.document_chain = create_stuff_documents_chain(
            llm=self.llm, prompt=self.prompt
        )

        # Add workflow manager
        self.workflow_manager = WorkflowManager(self)

    async def get_response(self, query: str, context: str) -> Dict:
        """
        Get response for a query using the provided context
        """
        try:
            # Convert context string to Document object
            doc = Document(page_content=context)

            # Get response using the document chain
            response = await self.document_chain.ainvoke(
                {"input": query, "context": [doc]}
            )
            return response
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            raise

    async def generate_stream(self, query: str, context: str):
        try:
            result = await self.workflow_manager.run_workflow(query, context)

            # If we have a calculation result, include it
            if "calculation_result" in result:
                yield f"data: {json.dumps({'text': f'Calculation: {result["calculation_result"]}', 'type': 'calculation'})}\n\n"

            # Yield the final response
            if result["final_response"]:
                yield f"data: {json.dumps({'text': result["final_response"], 'type': 'assistant'})}\n\n"

        except Exception as e:
            logger.error(f"Error in generate_stream: {str(e)}")
            yield f"data: {json.dumps({'text': f'Error: {str(e)}', 'type': 'error'})}\n\n"

from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from typing import AsyncIterator
import logging
from app.core.config import settings
import json

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Initialize LLM with streaming
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            streaming=True,
        )

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful AI assistant. Please analyze the following question using the provided context and respond accordingly.

            If the context contains relevant information:
            - Use ONLY the information from the context to answer
            - Quote relevant parts using "..." when appropriate
            - Cite specific sections or sources if available in the context

            If the context doesn't contain sufficient information:
            - Provide a general answer based on your knowledge
            Format your response in a clear, structured manner.
            
            
            If the user's question is relevant to the chat history, use the chat history to answer the question along with the context.
            If the user's question is not relevant to the chat history, use the context to answer the question.
            
            
            Always remember to use markdown to format the answer.

            Context:
            <context>
            {context}
            </context>

            Question: {input}

            """
        )

        self.document_chain = create_stuff_documents_chain(
            llm=self.llm, prompt=self.prompt
        )

    async def generate_stream(
        self, query: str, full_context: dict
    ) -> AsyncIterator[str]:
        try:
            yield f"data: {json.dumps({'text': 'Processing query...', 'type': 'system'})}\n\n"

            context_str = f"""
Chat History:
{full_context['chat_history']}

Retrieved Context:
{full_context['retrieved_context']}
"""

            # Process query with context
            doc = Document(page_content=context_str)
            async for chunk in self.document_chain.astream(
                {"input": query, "context": [doc]}
            ):
                if isinstance(chunk, str):
                    yield f"data: {json.dumps({'text': chunk, 'type': 'assistant'})}\n\n"
                else:
                    yield f"data: {json.dumps({'text': str(chunk), 'type': 'assistant'})}\n\n"

        except Exception as e:
            logger.error(f"Error in generate_stream: {str(e)}")
            yield f"data: {json.dumps({'text': f'Error: {str(e)}', 'type': 'error'})}\n\n"

    async def generate_query(self, prompt: str) -> str:
        try:
            non_streaming_llm = ChatOpenAI(
                api_key=self.api_key,
                model=settings.MODEL_NAME,
                temperature=0.3,
                streaming=False,
            )

            response = await non_streaming_llm.ainvoke(prompt)
            return response.content

        except Exception as e:
            logger.error(f"Error in generate_query: {str(e)}")
            raise

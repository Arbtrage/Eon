from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.config import get_settings

settings = get_settings()


class TextService:
    def __init__(self):
        print("🤖 Initializing Text Service with Gemini model...")
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_CHAT_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0,
        )

    def chunk_and_summarize(self, text: str) -> list[str]:
        print("📝 Starting text chunking and summarization...")

        summarizer_prompt = PromptTemplate(
            input_variables=["text"],
            template="Summarize the following content concisely: {text}",
        )

        summarizer_chain = LLMChain(llm=self.llm, prompt=summarizer_prompt)

        print("✂️  Splitting text into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        chunks = text_splitter.split_text(text)
        print(f"📚 Text split into {len(chunks)} chunks")

        summarized_chunks = []
        for i, chunk in enumerate(chunks, 1):
            print(f"📋 Summarizing chunk {i}/{len(chunks)}...")
            try:
                summary = summarizer_chain.run(chunk)
                summarized_chunks.append(summary)
            except Exception as e:
                print(f"❌ Error summarizing chunk {i}: {str(e)}")
                raise

        print("✅ Successfully completed text chunking and summarization")
        return summarized_chunks

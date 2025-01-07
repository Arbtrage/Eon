from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.core.config import get_settings
import re

settings = get_settings()

class TextService:
    def __init__(self):
        print("🤖 Initializing Text Service with OpenAI model...")
        self.llm = ChatOpenAI(
            model=settings.OPENAI_CHAT_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.5,
        )
        self.markdown_splitter = MarkdownTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
        )
        self.summarizer_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["text"],
                template="Summarize the following content concisely while preserving key information: {text}",
            ),
        )

    def is_markdown_content(self, text: str) -> bool:
        markdown_patterns = [
            r"^#+ ",
            r"^\s*[-*+] ",
            r"^\s*\d+\. ", 
            r"`{1,3}",
            r"\[.*\]\(.*\)",  
            r"\*\*.*\*\*",  
            r"_.*_", 
        ]

        for pattern in markdown_patterns:
            if re.search(pattern, text, re.MULTILINE):
                return True
        return False

    def process_text(self, text: str) -> list[str]:
        print("📝 Starting text processing...")

        if self.is_markdown_content(text):
            print("📑 Detected markdown content, using markdown-aware splitting...")
            primary_chunks = self.markdown_splitter.split_text(text)
            final_chunks = []
            for chunk in primary_chunks:
                if len(chunk) > 1000:
                    final_chunks.extend(self.recursive_splitter.split_text(chunk))
                else:
                    final_chunks.append(chunk)
        else:
            print("📄 Using recursive splitting for general content...")
            final_chunks = self.recursive_splitter.split_text(text)

        print(f"📚 Text split into {len(final_chunks)} chunks")
        
        summarized_chunks = []
        for i, chunk in enumerate(final_chunks, 1):
            print(f"📋 Processing chunk {i}/{len(final_chunks)}...")
            try:
                summary = self.summarizer_chain.run(chunk)
                summarized_chunks.append(summary)
            except Exception as e:
                print(f"❌ Error processing chunk {i}: {str(e)}")
                raise

        print("✅ Successfully completed text processing")
        return summarized_chunks

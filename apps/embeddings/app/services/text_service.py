from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter
from app.core.config import get_settings

settings = get_settings()

class TextService:
    def __init__(self):
        self.markdown_splitter = MarkdownTextSplitter(chunk_size=200, chunk_overlap=0)
        self.recursive_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=200,
            chunk_overlap=0,
            model_name="gpt-4o",
        )

    def process_text(self, text: str) -> list[str]:
        print("📝 Starting text processing...")
        # chunks = self.recursive_splitter.split_text(text)
        chunks = self.markdown_splitter.create_documents(text)
        print(f"📚 Text split into {len(chunks)} chunks")
        return chunks

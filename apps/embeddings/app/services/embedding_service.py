from langchain_openai import OpenAIEmbeddings
from app.core.config import get_settings
from app.core.exceptions import EmbeddingError

settings = get_settings()


class EmbeddingService:
    def __init__(self):
        print("🚀 Initializing Embedding Service with OpenAI model...")
        self.embeddings_model = OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )

    def create_embeddings(self, texts: list[str]) -> list:
        try:
            print(f"📊 Creating embeddings for {len(texts)} texts...")
            embeddings = self.embeddings_model.embed_documents(texts)
            print("✅ Successfully created embeddings")
            return embeddings
        except Exception as e:
            print(f"❌ Error creating embeddings: {str(e)}")
            raise EmbeddingError()

    def create_query_embedding(self, text: str) -> list:
        try:
            print("🔍 Creating embedding for search query...")
            embedding = self.embeddings_model.embed_query(text)
            print("✅ Successfully created query embedding")
            return embedding
        except Exception as e:
            print(f"❌ Error creating query embedding: {str(e)}")
            raise EmbeddingError()

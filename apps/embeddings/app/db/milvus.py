from pymilvus import (
    Collection,
    connections,
    utility,
    CollectionSchema,
    FieldSchema,
    DataType,
)
from app.core.config import get_settings
from app.core.exceptions import MilvusConnectionError

settings = get_settings()


class MilvusDB:
    def __init__(self):
        self.collection_name = settings.COLLECTION_NAME
        self.init_connection()

    def init_connection(self):
        try:
            print(
                f"🔌 Connecting to Milvus at {settings.MILVUS_HOST}:{settings.MILVUS_PORT}..."
            )
            connections.connect(
                "default", host=settings.MILVUS_HOST, port=settings.MILVUS_PORT
            )
            print("✅ Successfully connected to Milvus")
        except Exception as e:
            print(f"❌ Failed to connect to Milvus: {str(e)}")
            raise MilvusConnectionError()

    def create_collection(self):
        try:
            if self.collection_name not in utility.list_collections():
                print(f"📦 Creating new collection: {self.collection_name}")

                id_field = FieldSchema(
                    name="id", dtype=DataType.INT64, is_primary=True, auto_id=True
                )

                text_field = FieldSchema(
                    name="text", dtype=DataType.VARCHAR, max_length=500
                )

                embedding_field = FieldSchema(
                    name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768
                )

                schema = CollectionSchema(
                    fields=[id_field, text_field, embedding_field],
                    description="Text embeddings collection",
                )

                collection = Collection(
                    name=self.collection_name, schema=schema, using="default"
                )

                print("📊 Creating index for embeddings...")
                index_params = {
                    "metric_type": "L2",
                    "index_type": "IVF_FLAT",
                    "params": {"nlist": 1024},
                }
                collection.create_index(
                    field_name="embedding", index_params=index_params
                )
                print("✅ Successfully created collection and index")

                return collection
            else:
                print(f"📂 Using existing collection: {self.collection_name}")
                return Collection(self.collection_name)
        except Exception as e:
            print(f"❌ Error creating/accessing collection: {str(e)}")
            raise

    def get_collection(self):
        try:
            print(f"🔍 Getting collection: {self.collection_name}")
            return Collection(self.collection_name)
        except Exception as e:
            print(f"❌ Error getting collection: {str(e)}")
            raise

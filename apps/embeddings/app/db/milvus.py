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

                fields = [
                    FieldSchema(
                        name="id", dtype=DataType.INT64, is_primary=True, auto_id=True
                    ),
                    FieldSchema(name="user_id", dtype=DataType.VARCHAR, max_length=64),
                    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
                    FieldSchema(
                        name="embedding",
                        dtype=DataType.FLOAT_VECTOR,
                        dim=1536,
                    ),
                ]

                schema = CollectionSchema(
                    fields=fields,
                    description="User-specific text embeddings collection",
                    enable_dynamic_field=True,  
                )

                collection = Collection(
                    name=self.collection_name, schema=schema, using="default"
                )

                print("📊 Creating indexes...")
                index_params = {
                    "metric_type": "L2",
                    "index_type": "IVF_FLAT",
                    "params": {"nlist": 1024},
                }
                collection.create_index(
                    field_name="embedding", index_params=index_params
                )

                collection.create_index(
                    field_name="user_id",
                    index_name="user_id_index",
                    index_params={"index_type": "Trie"},
                )

                print("✅ Successfully created collection and indexes")
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

    def insert_embeddings(
        self, user_id: str, texts: list[str], embeddings: list[list[float]]
    ):
        try:
            collection = self.get_collection()
            collection.load()

            entities = [
                {"user_id": user_id, "text": text, "embedding": embedding}
                for text, embedding in zip(texts, embeddings)
            ]

            print(f"📥 Inserting {len(texts)} embeddings for user {user_id}")
            collection.insert(entities)
            collection.flush()
            print("✅ Successfully inserted embeddings")
        except Exception as e:
            print(f"❌ Error inserting embeddings: {str(e)}")
            raise
        finally:
            collection.release()

    def search_similar(
        self,
        user_id: str,
        query_embedding: list[float],
        limit: int = 5,
        score_threshold: float = 0.5,
    ) -> list[dict]:
        try:
            collection = self.get_collection()
            collection.load()


            search_params = {
                "metric_type": "L2",
                "params": {"nprobe": 16},
            }

            results = collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=limit,
                expr=f'user_id == "{user_id}"',
                output_fields=["text", "user_id"],
            )

            similar_docs = []
            for hits in results:
                print(f"\n📝 Raw search results: {len(hits)} hits")
                for hit in hits:
                    similarity = 1 / (1 + hit.distance)
                    print(f"🎯 Hit details:")
                    print(f"  - Distance: {hit.distance}")
                    print(f"  - Similarity score: {similarity}")
                    print(f"  - User ID: {hit.entity.get('user_id')}")
                    print(f"  - Text preview: {hit.entity.get('text')[:50]}...")
                    similar_docs.append(
                        {
                            "text": hit.entity.get("text"),
                            "score": similarity,
                            "user_id": hit.entity.get("user_id"),
                            "distance": hit.distance,
                        }
                    )
            similar_docs.sort(key=lambda x: x["score"], reverse=True)

            filtered_docs = [
                doc for doc in similar_docs if doc["score"] >= score_threshold
            ]

            print(f"\n📊 Search results summary:")
            print(f"  - Total hits: {len(similar_docs)}")
            print(f"  - Hits above threshold: {len(filtered_docs)}")

            return filtered_docs

        except Exception as e:
            print(f"❌ Error searching embeddings: {str(e)}")
            raise
        finally:
            collection.release()

    # def list_data(self):
    #     """
    #     List all data present in the collection with their attributes.
    #     """
    #     try:
    #         collection = self.get_collection()
    #         collection.load()

    #         print(f"📊 Total entities in collection: {collection.num_entities}")

    #         # Query all data
    #         results = collection.query(
    #             expr="user_id != ''",  # Query all records
    #             output_fields=["user_id", "text"],  # Fields to retrieve
    #             limit=collection.num_entities,  # Get all records
    #         )

    #         print("\n📝 Collection contents:")
    #         for idx, item in enumerate(results, 1):
    #             print(f"\nRecord {idx}:")
    #             print(f"User ID: {item['user_id']}")
    #             print(f"Text: {item['text'][:100]}...")  # Show first 100 chars of text

    #         return results

    #     except Exception as e:
    #         print(f"❌ Error listing data: {str(e)}")
    #         raise
    #     finally:
    #         collection.release()

from src.data import IDatabase
from src.models import GameReviewEmbeddings


class EmbeddingsService:
    @classmethod
    def insert(
        cls,
        embeddings_data: GameReviewEmbeddings,
        database: IDatabase):

        pass

    @classmethod
    def create_table(cls, database: IDatabase):
        with database.get_cursor() as cursor:
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS embeddings_data.table_name (embedding, review_id)"""
            )
    # with database.get_cursor() as cursor:
    #   cursor.execute(
    #       f"""INSERT INTO embeddings_data.table_name (embedding, review_id) VALUES (?, ?)""",
    #       (embeddings_data.embedding, embeddings_data.reviews)
    #   )
    #   cursor.commit()

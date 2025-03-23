from sqlalchemy import Column, Text, Integer
from pgvector.sqlalchemy import Vector
from client.db_client import Base

class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    content = Column(Text)
    embeddings = Column(Vector(1536))
import os
import logging
from uuid import uuid4
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader

load_dotenv()

base_url = "https://api.us.inc/usf/v1/hiring"

US_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
RECORDS_DIR_PATH = os.getenv("RECORDS_DIR_PATH")

'''
RAG: Retrieval-Augmented Generation class for handling document embeddings and QA.
'''
class RAG:
    def __init__(
        self, doc_path: str = None, pinecone_index: str = "medical-records-index"
    ):
        self.doc_path = doc_path
        self.pinecone_index = pinecone_index
        self.vector_store = None

    def load_all_docs(self, dir_path):
        documents = []
        p = Path(dir_path)
        files_path = [f.name for f in p.iterdir() if f.is_file()]
        for fpath in files_path:
            ext = os.path.splitext(fpath)[-1].lower()
            if ext == ".pdf":
                logging.info(f"Loading document: {dir_path+fpath}")
                loader = PyPDFLoader(dir_path + fpath)
                docs = loader.load()
                documents.extend(docs)
            elif ext == ".txt":
                loader = TextLoader(dir_path + fpath)
                docs = loader.load()
                documents.extend(docs)
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        return documents

    def create_faiss_embeddings(self):
        embeddings = OpenAIEmbeddings()
        loader = PyPDFLoader(self.doc_path)
        self.documents = loader.load()
        self.vector_store = FAISS.from_documents(self.documents, embeddings)

    def create_pinecone_embeddings(self):
        # Initialize Pinecone client
        pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
        # pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

        index_name = self.pinecone_index

        index = pc.Index(index_name)

        # Create index if it does not exist
        if not pc.has_index(index_name):
            # Assuming embedding dimension 1536 for OpenAI embeddings
            logging.info(f"Creating Pinecone index: {index_name}")
            pc.create_index(
                name=index_name,
                dimension=1536,
                vector_type="dense",
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        embeddings = OpenAIEmbeddings()
        all_docs = self.load_all_docs(RECORDS_DIR_PATH)
        self.vector_store = PineconeVectorStore(index=index, embedding=embeddings)
        uuids = [str(uuid4()) for _ in range(len(all_docs))]
        self.vector_store.add_documents(documents=all_docs, ids=uuids)

    def create_qa_chain(self):
        llm = OpenAI(temperature=0)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(),
        )

    def query(self, query: str):
        answer = self.qa_chain.invoke(query)
        return answer["result"]

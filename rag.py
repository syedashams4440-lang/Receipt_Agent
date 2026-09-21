from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def create_vector_store():

    documents = []

    return_loader = TextLoader(
        "data/return_policy.txt",
        encoding="utf-8"
    )

    warranty_loader = TextLoader(
        "data/warranty_policy.txt",
        encoding="utf-8"
    )

    documents.extend(return_loader.load())
    documents.extend(warranty_loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_store


def create_retriever():

    vector_store = create_vector_store()

    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )
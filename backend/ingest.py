import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# Define the paths and metadata mapping
DATA_DIR = "../Sample_data"
DB_DIR = "./chroma_db"

FILE_MAPPING = {
    "hiring_policy.md": "hr",
    "open_roles.md": "hr",
    "marketing_budget.md": "marketing",
    "q3_campaign_report.md": "marketing",
    "q3_budget.md": "finance",
    "spend_approval_policy.md": "finance"
}

def ingest_data():
    print("Starting data ingestion and chunking...")
    documents = []
    
    # 1. Load documents and add department metadata
    for filename, dept in FILE_MAPPING.items():
        file_path = os.path.join(DATA_DIR, filename)
        if os.path.exists(file_path):
            loader = TextLoader(file_path, encoding='utf-8')
            docs = loader.load()
            # Inject metadata
            for doc in docs:
                doc.metadata["department"] = dept
                doc.metadata["source"] = filename
            documents.extend(docs)
            print(f"Loaded {filename} for {dept} department.")
        else:
            print(f"Warning: {filename} not found in {DATA_DIR}")

    # 2. Chunk the documents
    # Using a relatively small chunk size since the docs are short and dense
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # 3. Embed and store in Chroma
    # We use a lightweight local open-source embedding model for speed
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Initializing Chroma DB and storing embeddings...")
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_function, 
        persist_directory=DB_DIR
    )
    
    print(f"Success! Data embedded and saved to {DB_DIR}")

if __name__ == "__main__":
    ingest_data()

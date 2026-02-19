import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ollama import Client
import chromadb

# 1. Initialize the local Vector Database (ChromaDB)
client = chromadb.Client()
remote_client = Client(host=f'http://localhost:11434')

splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=0,
    separators=['.','\n']
)

collection = client.get_or_create_collection(name="simple_knowledge")

collection = client.get_or_create_collection(
    name="simple_knowledge",
    metadata={"hnsw:space": "cosine"}
)

# 2. Load the simple text file and embed each line
# print("Reading simple.txt and generating embeddings...")

with open('articles.jsonl', 'r',encoding='utf-8') as f:
    for i, line in enumerate(f):
        content=json.loads(line)
        content=content['content']
        chunks=[c.strip() for c in splitter.split_text(content)]
        for j, c in enumerate(chunks):
        
         response = remote_client.embed(model='nomic-embed-text', input=c)
        # response = remote_client.embed(model='nomic-embed-text', input=f"search_document: {content}")
        
        embedding = response['embeddings'][0]
        collection.add(
            ids=[f"id_{i}_{j}"],
            embeddings=[embedding],
            documents=[c],
            metadatas=[{"line": j}]
        )

print("Database built successfully!")

# 3. Test Retrieval
query = "are there any predicted hindrance for upcoming election ?"

query_embed = remote_client.embed(model='nomic-embed-text', input=query)['embeddings'][0]
# query_embed = remote_client.embed(
#     model='nomic-embed-text', 
#     input=f"search_query: {query}"
# )['embeddings'][0]

results = collection.query(
    query_embeddings=[query_embed],
    n_results=1
)

print(f"\nQuestion: {query}")
print(f"Retrieved Context: {results['documents'][0][0]}")

# After stationing vehicle on ground, leave money on gate.
# Pay for dinner using company app.
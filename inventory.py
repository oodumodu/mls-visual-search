import chromadb

# Connect to the database
chroma_client = chromadb.PersistentClient(path="./mls_vector_db")
collection = chroma_client.get_collection(name="mls_listings")

# Get all data (limit to 25 just to be safe)
results = collection.get(limit=25)
metadatas = results['metadatas']

print(f"--- DUMPING INVENTORY ({len(metadatas)} items) ---")

for i, data in enumerate(metadatas):
    print(f"\n{i+1}. {data['address']}")
    print(f"   {data['image_url']}")

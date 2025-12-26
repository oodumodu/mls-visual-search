import chromadb
# Pointing to the CORRECT folder name from your ingest script
client = chromadb.PersistentClient(path="./mls_vector_db") 

print("Collections found:", client.list_collections())

# specific check for the collection count
try:
    coll = client.get_collection("mls_listings")
    print(f"Item count: {coll.count()}")
except Exception as e:
    print(f"Could not find collection: {e}")
import chromadb
from sentence_transformers import SentenceTransformer

# --- CONFIGURATION ---
# The "Unicorn Line" was 160. We set the limit slightly lower
# to filter out nonsense while keeping weak matches.
DISTANCE_THRESHOLD = 158 

# --- 1. LOAD SYSTEM ---
print("Loading model...")
model = SentenceTransformer('clip-ViT-B-32')

chroma_client = chromadb.PersistentClient(path="./mls_vector_db")
collection = chroma_client.get_collection(name="mls_listings")

def search_homes(user_query):
    print(f"\n🔍 Searching for: '{user_query}'...")
    
    query_vector = model.encode(user_query).tolist()
    
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )
    
    ids = results['ids'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]
    
    found_any = False

    for i in range(len(ids)):
        dist = distances[i]
        
        # Filter out anything worse than a "weak match"
        if dist > DISTANCE_THRESHOLD:
            continue

        found_any = True
        data = metadatas[i]
        
        # CALIBRATED SCORING:
        # Best match seen was ~139. Worst accepted is 158.
        # We map this range (139-158) to a 0-100% scale.
        score_percent = max(0, min(100, (1 - (dist - 139) / (158 - 139)) * 100))

        print(f"\n--- Match {i+1} (Confidence: {score_percent:.0f}%) ---")
        print(f"🏠 Address: {data['address']}")
        print(f"💰 Price:   ${data['price']:,}")
        print(f"🖼️  Image:   {data['image_url']}")

    if not found_any:
        print("\n❌ No homes found matching that description.")

if __name__ == "__main__":
    print("--- Local MLS Vector Search (Type 'exit' to quit) ---")
    while True:
        try:
            user_input = input("\nDescribe the home: ")
            if user_input.lower() in ['exit', 'quit']: 
                break
            if user_input.strip() == "":
                continue
            search_homes(user_input)
        except KeyboardInterrupt:
            break
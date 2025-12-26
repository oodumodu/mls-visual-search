import requests
import chromadb
from sentence_transformers import SentenceTransformer
from PIL import Image
from io import BytesIO

# --- 1. CONFIGURATION ---
# The Secret Public Demo Credentials (No signup needed)
API_URL = "https://api.simplyrets.com/properties"
AUTH = ('simplyrets', 'simplyrets') 

# --- 2. SETUP AI & DATABASE ---
print("Loading CLIP Model... (Downloads ~600MB the first time)")
model = SentenceTransformer('clip-ViT-B-32')

print("Initializing Local Database...")
# This creates a folder "./mls_vector_db" to store data
chroma_client = chromadb.PersistentClient(path="./mls_vector_db")
collection = chroma_client.get_or_create_collection(name="mls_listings")

# --- 3. FETCH & PROCESS ---
print("Fetching listings from SimplyRETS Demo...")
response = requests.get(API_URL, auth=AUTH)
listings = response.json()

print(f"Found {len(listings)} listings. Processing images...")

count = 0
for house in listings:
    mls_id = str(house.get('mlsId'))
    address = house.get('address', {}).get('full')
    price = house.get('listPrice')
    
    # Get the first photo URL
    photos = house.get('photos', [])
    if not photos:
        continue
    image_url = photos[0] 
    
    try:
        # A. Download Image into Memory
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))
        
        # B. AI "Looks" at the image -> Creates Vector
        vector = model.encode(img).tolist()
        
        # C. Save to Local Database
        collection.add(
            ids=[mls_id],
            embeddings=[vector],
            metadatas=[{
                "price": price, 
                "address": address, 
                "image_url": image_url
            }]
        )
        print(f"✅ Indexed: {address} (${price})")
        count += 1
        
    except Exception as e:
        print(f"❌ Error on {mls_id}: {e}")

print(f"\nSUCCESS! Indexed {count} listings into './mls_vector_db'.")
# 🏡 AI-Powered MLS Visual Search

An intelligent real estate search engine that allows users to search for homes using natural language descriptions of visual features (e.g., "brick house," "modern kitchen," "large yard"). 

Unlike traditional filters (Price, Beds, Baths), this project uses **Multimodal AI (CLIP)** to "see" listing photos and index them into a local vector database.

## 🚀 How It Works
1.  **Ingestion:** The system pulls live real estate data from the SimplyRETS Demo API.
2.  **Vectorization:** It uses OpenAI's `clip-ViT-B-32` model to convert listing photos into 512-dimensional vector embeddings.
3.  **Storage:** Embeddings are stored locally in **ChromaDB**.
4.  **Retrieval:** When a user searches for "brick house," the text is converted to a vector, and the system finds the nearest image vectors using cosine similarity.

## 🛠️ Tech Stack
* **Python 3.10+**
* **ChromaDB:** Local open-source vector database.
* **Sentence-Transformers:** For implementing the CLIP model.
* **Pillow (PIL):** Image processing.
* **SimplyRETS API:** Source of MLS data.

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/oodumodu/mls-visual-search.git](https://github.com/oodumodu/mls-visual-search.git)
    cd mls-visual-search
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃 Usage

**1. Index the Data**
Run the ingestion script to download listings and generate vectors.
```bash
python ingest.py
```
*Note: The first run downloads the ~600MB CLIP model.*

**2. Search**
Run the interactive search tool.
```bash
python search.py
```

## 🧠 Technical Highlights
* **Zero-Shot Classification:** The model was never trained on real estate specifically, yet understands concepts like "curb appeal" or "driveway" out of the box.
* **Vector Space Calibration:** Includes a custom diagnostic mode to calibrate distance thresholds, filtering out low-confidence matches (e.g., "dragons").

## 📄 License
MIT

# AI-Driven Visual Search Platform
# Requirements: Python 3.7+, PyTorch, transformers, Pillow, pinecone-client, fastapi

import os
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import List, Dict
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import uvicorn
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import traceback
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import shutil

# Load environment variables
load_dotenv()

# Initialize CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Initialize Pinecone
# You'll need to sign up for Pinecone and get an API key
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("Please set PINECONE_API_KEY in your .env file")

PINECONE_ENV = os.getenv("PINECONE_ENV", "gcp-starter")

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "image-search"

# Add this before creating the index
print("Available indexes:", pc.list_indexes().names())
print("Creating index in starter environment...")

# Check if index exists and create if it doesn't
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=512,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)

app = FastAPI()

# Add these near the top where you create the FastAPI app
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create uploads directory if it doesn't exist
os.makedirs("static/uploads", exist_ok=True)

class SearchQuery(BaseModel):
    text_query: str = None
    image_id: str = None
    top_k: int = 5

def get_image_embedding(image_path: str) -> torch.Tensor:
    """Generate CLIP embedding for an image."""
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt", padding=True)
    image_features = model.get_image_features(**inputs)
    # Convert to numpy, flatten, and ensure we have a 1D array of floats
    embedding = image_features.detach().numpy().flatten().astype('float32')
    print(f"Embedding shape: {embedding.shape}")  # Debug print
    print(f"Embedding type: {embedding.dtype}")   # Debug print
    print(f"First few values: {embedding[:5]}")   # Debug print
    return embedding

def get_text_embedding(text: str) -> torch.Tensor:
    """Generate CLIP embedding for text."""
    inputs = processor(text=text, return_tensors="pt", padding=True)
    text_features = model.get_text_features(**inputs)
    return text_features.detach().numpy()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...), tags: List[str] = None):
    try:
        # Save file to uploads directory
        file_path = f"static/uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get embedding
        embedding = get_image_embedding(file_path)
        
        # Store in Pinecone with full URL path
        image_url = f"/static/uploads/{file.filename}"
        vector_data = {
            'id': file.filename,
            'values': embedding.tolist(),
            'metadata': {
                "filename": file.filename,
                "image_url": image_url,  # Store the full URL path
                "tags": tags or []
            }
        }
        
        index.upsert(vectors=[vector_data])
        return {"message": "Image uploaded and indexed successfully", "image_url": image_url}
    except Exception as e:
        print(f"Error in upload_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search(query: SearchQuery):
    """Search for similar images using text or image query."""
    if query.text_query and query.image_id:
        raise HTTPException(
            status_code=400, 
            detail="Please provide either text_query OR image_id, not both"
        )
        
    if query.text_query:
        # Text-based search
        query_embedding = get_text_embedding(query.text_query)
        query_embedding = query_embedding.flatten()  # Ensure 1D array
    elif query.image_id:
        # Image-based search
        vector = index.fetch(ids=[query.image_id])
        if not vector:
            raise HTTPException(status_code=404, detail="Image not found")
        query_embedding = vector[query.image_id].values
    else:
        raise HTTPException(
            status_code=400,
            detail="Must provide either text_query or image_id"
        )
    
    # Search Pinecone
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=query.top_k,
        include_metadata=True
    )
    
    # Convert results to a simple dict format
    return {
        "matches": [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            }
            for match in results.matches
        ]
    }

# Add this new endpoint
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

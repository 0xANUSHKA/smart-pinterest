import os
import json
from SmartPinterest import get_image_embedding, index
from PIL import Image

def index_local_images(directory='static/uploads'):
    """Index all images in the uploads directory with metadata"""
    
    # Load metadata if it exists
    metadata_file = os.path.join(directory, 'metadata.json')
    metadata = {}
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(directory, filename)
            
            try:
                # Get embedding
                embedding = get_image_embedding(filepath)
                
                # Get metadata for this image
                image_meta = metadata.get(filename, {
                    "tags": ["scraped"],
                    "description": filename
                })
                
                # Store in Pinecone
                image_url = f"/static/uploads/{filename}"
                vector_data = {
                    'id': filename,
                    'values': embedding.tolist(),
                    'metadata': {
                        "filename": filename,
                        "image_url": image_url,
                        "tags": image_meta["tags"],
                        "description": image_meta["description"],
                        "author": image_meta.get("author", "unknown")
                    }
                }
                
                index.upsert(vectors=[vector_data])
                print(f'Indexed: {filename} with tags: {image_meta["tags"]}')
                
            except Exception as e:
                print(f'Error indexing {filename}: {e}')

if __name__ == "__main__":
    index_local_images() 
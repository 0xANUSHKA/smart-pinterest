import requests
import os
import time
import json
import random

def download_images(save_dir='static/uploads', max_images=100, start_id=0):
    """Download images from Lorem Picsum with metadata"""
    
    os.makedirs(save_dir, exist_ok=True)
    metadata_file = os.path.join(save_dir, 'metadata.json')
    image_metadata = {}
    
    # Get list of all available images first
    print("Getting list of available images...")
    list_url = "https://picsum.photos/v2/list?limit=100"
    image_list = requests.get(list_url).json()
    
    # Shuffle the list for variety
    random.shuffle(image_list)
    
    for i, image_info in enumerate(image_list[:max_images]):
        try:
            # Get high resolution image
            width = 1200  # larger size
            height = 800
            img_url = f"https://picsum.photos/id/{image_info['id']}/{width}/{height}"
            img_data = requests.get(img_url).content
            
            # Save image
            filename = f'image_{start_id + i}.jpg'
            filepath = os.path.join(save_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(img_data)
            
            # Store rich metadata
            image_metadata[filename] = {
                "author": image_info["author"],
                "url": image_info["url"],
                "tags": [
                    "photo",
                    image_info["author"].lower().replace(" ", "-"),
                    f"width-{image_info['width']}",
                    f"height-{image_info['height']}",
                    "high-quality"
                ],
                "description": f"High quality photo by {image_info['author']}",
                "original_width": image_info["width"],
                "original_height": image_info["height"],
                "download_url": image_info["download_url"]
            }
            
            print(f'Downloaded ({i+1}/{max_images}): {filename} by {image_info["author"]}')
            time.sleep(0.5)  # Be nice to the server
            
        except Exception as e:
            print(f'Error downloading image {i}: {e}')
            continue
    
    # Save metadata
    with open(metadata_file, 'w') as f:
        json.dump(image_metadata, f, indent=2)
            
    print(f'Download complete! Metadata saved to {metadata_file}')

def download_multiple_batches(total_images=500, batch_size=100):
    """Download multiple batches of images"""
    for i in range(0, total_images, batch_size):
        print(f"\nDownloading batch {(i//batch_size)+1}...")
        download_images(max_images=batch_size, start_id=i)
        time.sleep(2)  # Pause between batches

if __name__ == "__main__":
    # Download 500 images in batches of 100
    download_multiple_batches(total_images=500, batch_size=100) 
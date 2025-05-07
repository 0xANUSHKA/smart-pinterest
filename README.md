# Smart Pinterest - Proof of Concept

An AI-powered visual search engine that uses CLIP and neural embeddings to understand images like humans do. Search for images using natural language, emotions, and abstract concepts.

## Why I Built This

As a long-time Pinterest user and fan, I've spent a lot of time curating boards and searching for inspo. While Pinterest is amazing for discovering products and ideas, I often found myself thinking: "I wish I could find images that _feel_ like this" or "I want something that captures this mood, but I don't know the right words to search for it."

That's when it hit me - what if we could search for images the way we naturally think about them?

This project isn't about replacing Pinterest, it's about exploring a different way of discovering visual content. One that's less about shopping and trends, and more about pure visual understanding and emotional connection.

## How it differs from Pinterest

### Pinterest's Current AI Approach:

- Uses specialized computer vision models trained on user engagement data
- Combines multiple AI systems: object detection, visual search, recommendation engines
- Focuses on product recognition and shopping integration
- Relies on a mix of user behavior data and image content
- Optimized for engagement and commercial intent

### My "Smart Pinterest" Approach:

- **Single Unified Model**: Uses CLIP's multimodal understanding instead of multiple specialized systems
- **Zero-Shot Learning**: Can understand new concepts without specific training
- **Pure Content Understanding**: Focuses on semantic meaning rather than user behavior patterns
- **Academic vs Commercial**: Uses research-focused models that prioritize understanding over engagement
- **Transparent Search**: Results based purely on image-text similarity, not influenced by commercial factors

For example, when searching on Pinterest:

- Results are influenced by popularity and commercial relevance
- Recommendations mix visual similarity with user behavior patterns
- Search understanding is optimized for shopping and DIY projects

With this system:

- Results are based purely on semantic understanding
- Finds matches based on actual visual and conceptual content
- Can understand abstract ideas without prior examples

### Key Technical Differences:

- **Model Architecture**: We use CLIP's transformer-based architecture for unified understanding
- **Vector Space**: All concepts (images and text) live in the same high-dimensional space
- **Raw Understanding**: No fine-tuning for commercial purposes or engagement metrics
- **Direct Matching**: Pure similarity search without recommendation system modifications

## Features

### Natural Language Search

- Search using everyday language
- Find images based on concepts and feelings
- No need for exact tag matches

### AI-Powered Understanding

- Powered by OpenAI's CLIP model
- Understands both images and text
- Recognizes artistic styles and abstract concepts

### Smart Similarity Search

- Find visually similar images
- Search by example image
- Discover related content intelligently

## 🚀 Getting Started

1. **Clone and Setup**

git clone https://github.com/yourusername/smart-pinterest
cd smart-pinterest
python -m venv venv
source venv/bin/activate # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

2. **Configure Environment**
   Create a `.env` file:

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=gcp-starter

3. **Download and Index Images**

python scrape_images.py # Get initial image set
python index_images.py # Index them for search

4. **Run the App**
   python SmartPinterest.py

Visit `http://localhost:8000` in your browser

## 🔍 Features

- **Natural Language Search**: Describe what you're looking for in plain words
- **Semantic Understanding**: Find images based on feelings and concepts
- **Visual Similarity**: Discover related images through AI understanding

## 🛠️ Technical Stack

- **Frontend**: HTML/CSS
- **Backend**: FastAPI + Python
- **AI**: OpenAI's CLIP model
- **Vector Search**: Pinecone
- **Image Source**: Lorem Picsum API

## 📝 Requirements

- Python 3.11+
- Pinecone API key
- 2GB disk space (for CLIP model)
- Modern web browser

## 🤔 Troubleshooting

**No images showing?**

- Run `scrape_images.py` and `index_images.py` first
- Check your Pinecone API key in `.env`

**Slow search?**

- First search is slow (CLIP loading)
- Subsequent searches are faster

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- [OpenAI CLIP](https://github.com/openai/CLIP)
- [Pinecone](https://www.pinecone.io/)
- [Lorem Picsum](https://picsum.photos/)

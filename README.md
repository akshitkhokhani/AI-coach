# 🧠 Mental Health Counseling Assistant

![GitHub stars](https://img.shields.io/github/stars/yourusername/mental-health-assistant?style=social)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)
![Next.js](https://img.shields.io/badge/Next.js-14.0-black)

> An AI-powered mental health counseling assistant that provides empathetic and supportive responses based on professional counseling examples.

<p align="center">
  <img src="[https://via.placeholder.com/800x400?text=Mental+Health+Assistant](https://ai-mental-health-coach.streamlit.app/)" alt="Mental Health Assistant Demo" width="800">
</p>

## ✨ Features

- 🤖 AI-powered mental health guidance using GPT-4o
- 🔍 Semantic search for similar counseling examples
- 📱 Responsive web interface built with Streamlit
- 📊 Alternative Streamlit interface for quick deployment
- 🔄 Real-time API with FastAPI
- 🔒 Environment variable configuration
- 📚 Vector database integration with Pinecone

## 🚀 Live Demo

[[Check out the live demo](https://ai-mental-health-coach.streamlit.app/)](https://ai-mental-health-coach.streamlit.app/)

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.9+
- **AI Models**: OpenAI GPT-4
- **Vector Database**: Pinecone
- **Frontend**: Streamlit
- **Embeddings**: FAISS, Sentence-Transformers

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Pinecone API key and index setup

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/akshitkhokhani/AI-coach.git
cd mental-health-assistant
```

### 2. Backend Setup

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (see .env.example)
cp .env.example .env
# Edit .env with your API keys
```

### 3. Frontend Setup

```bash
cd frontend
npm install
# Set up environment variables if needed
cp .env.example .env.local  # Then edit if necessary
```

## 🚀 Running the Application

### 1: Run Backend (FastAPI) and Frontend

#### Start the Backend API

```bash
# From the project root
python run.py
```

The API will be available at http://localhost:8000 with documentation at http://localhost:8000/api/v1/docs


### 2: Run with Streamlit UI

```bash
# From the project root
python run_streamlit.py
```

The Streamlit interface will be available at http://localhost:8501

## 🌱 Getting Started

### 1. Load Training Data

Before using the system, you need to load counseling examples into the vector database:

```bash
python load_data.py
```

### 2. Configuration Details

Create a `.env` file based on the example below:

```
# OpenAI credentials
OPENAI_API_KEY=your_openai_api_key_here

# Vector database settings
VECTOR_DB_TYPE=pinecone
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
PINECONE_INDEX_NAME=llama-text-embed-v2-index
PINECONE_NAMESPACE=counseling

# Embedding model settings
EMBEDDING_MODEL=llama-text-embed-v2
EMBEDDING_MODEL_SOURCE=pinecone

# Data path
DATASET_PATH=train.csv
```

## 📁 Project Structure

```
mental-health-assistant/
├── app/                    # FastAPI application
│   ├── api/                # API endpoints
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   ├── config.py           # Configuration
│   └── main.py             # FastAPI app initialization
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/            # Next.js app directory
│   │   ├── components/     # React components
│   │   └── lib/            # Utilities and API clients
├── venv/                   # Virtual environment
├── .env                    # Environment variables
├── .env.example            # Example environment variables
├── load_data.py            # Script to load data into vector DB
├── requirements.txt        # Python dependencies
├── run.py                  # Script to run FastAPI server
├── run_streamlit.py        # Script to run Streamlit interface
├── streamlit_app.py        # Streamlit application
└── README.md               # This file
```

## 📝 API Documentation

Once the FastAPI server is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### Key Endpoints

- `POST /api/v1/query` - Submit a mental health query and get a counseling response
- `GET /api/v1/status` - Check API health

## 🔒 Creating a Secure Pinecone Index

1. Sign up for a Pinecone account at [pinecone.io](https://www.pinecone.io/)
2. Create a new index with the following settings:
   - Name: `llama-text-embed-v2-index`
   - Dimensions: `1024`
   - Metric: `cosine`
   - Environment: Select a region close to your API deployment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📃 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [OpenAI](https://openai.com/) for GPT-4 API
- [Pinecone](https://www.pinecone.io/) for vector database
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/akshitkhokhani">Akshit Khokhani</a>
</p>

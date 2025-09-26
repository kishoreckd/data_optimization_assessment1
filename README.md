#Azure Data Optimization Microservice

A FastAPI-based microservice that processes and optimizes data records using machine learning (DistilBERT sentiment analysis), NLP (spaCy NER), and reinforcement learning (Q-learning).

The service supports data ingestion, cleaning, anonymization, metadata extraction, and refined rating generation, with optional simulated blob storage.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.13-green.svg?style=for-the-badge&logo=fastapi&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-3.8.0-blue.svg?style=for-the-badge&logo=spacy&logoColor=white)
![Transformers](https://img.shields.io/badge/Transformers-4.44.0-orange.svg?style=for-the-badge&logo=huggingface&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0.0-blue.svg?style=for-the-badge&logo=pandas&logoColor=white)
</div>


## 🚀 Features

- **Data Ingestion & Cleaning**: Automated data cleaning with missing value imputation
- **Natural Language Processing**: Named Entity Recognition (NER) using spaCy
- **Sentiment Analysis**: Text sentiment prediction using Hugging Face transformers
- **Q-Learning Optimization**: Reinforcement learning-based rating refinement
- **Data Anonymization**: Automatic masking of personal information
- **Blob Storage Simulation**:Local simulation of Azure Blob Storage
- **Rate Limiting**: API rate limiting with configurable limits

## 🏗️ Architecture

The service follows a modular architecture with the following components:

```
app/
   api/routes/         # API endpoints
      route.py         # router file 
   core/               # Config & settings
      config.py        # Config file for env data, const
      startup.py       # starting up the lifespan
   models/             # Pydantic models
      record_model.py  # Record Model for storing data
   service/            # Business logic
     ml/
       sentiment.py    # distilbert-base Model Pipeline
     ingestion.py      # Cleaning & imputation
     meta_data.py      # Metadata extraction (NER)
     ml_refine.py      # Sentiment + Q-learning refinement
     blob_storage.py   # Blob storage simulation
   utils/validation/    # Authentication and validation
     auth.py           #Auth validation
     json_validator    # response and error validation,(json)
```

## 📋 Prerequisites

- Python 3.12+
- spaCy English model
- Required Python packages (see installation section)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd azure-testapp
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn pandas numpy spacy transformers torch pydantic pydantic-settings python-dotenv
   ```

4. **Download spaCy English model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   AUTH_TOKEN=your-secure-token-here
   ```

## 🚀 Running the Application

1. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

2. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📡 API Endpoints

### POST `/optimize`
Processes a list of records through the complete optimization pipeline.

**Request Body:**
```json
[
  {
    "text": "This product is amazing!",
    "rating": 8.5,
    "timestamp": "2024-01-01T00:00:00Z"
  }
]
```

**Response:**
```json
{
  "success": true,
  "message": "Workflow completed successfully",
  "data": {
    "Total records processed": 1
  }
}
```

### GET `/retrieve`
Retrieve the final processed records from the system with pagination support (requires API key).

**Headers:**
```
api-key: your-api-key-here
```

**Query Parameters:**
- `page` (int, optional): Page number (default: 1, minimum: 1)
- `per_page` (int, optional): Records per page (default: 5, range: 1-100)

**Response:**
```json
{
  "success": true,
  "message": "Final records retrieved",
  "data": {
    "records": [...],
    "total_records": 50,
    "total_pages": 10,
    "page": 1,
    "per_page": 5
  }
}
```

### GET `/health`
Health check endpoint that returns the current UTC time.

**Response:**
```json
{
  "success": true,
  "message": "Service healthy",
  "data": {
    "time": "2024-01-01T12:00:00.000000+00:00"
  }
}
```



## 🧠 Machine Learning Components
### Sentiment Analysis
- Uses Hugging Face transformers pipeline
- Converts sentiment scores to 0-10 rating scale
- Handles text truncation for long inputs

### Q-Learning Agent
- Reinforcement learning for rating optimization
- Actions: [-1, 0, 1] (decrease, maintain, increase)
- State: rounded predicted rating
- Reward: based on accuracy vs actual ratings

### Named Entity Recognition
- spaCy-based NER for entity extraction
- Automatic masking of PERSON entities
- Metadata extraction for each record

## 📁 Data Flow

1. **Ingestion**: Raw records → Data cleaning → Imputed ratings
2. **Metadata Extraction**: Text → NER → Entity metadata
3. **ML Refinement**: Sentiment analysis → Q-learning → Optimized ratings
4. **Anonymization**: Text → Masked personal information
5. **Storage**: Processed records → Blob storage simulation


## 🧪 Testing

Test the API endpoints using curl or any HTTP client:

```bash
# Health check
curl http://localhost:8000/health

# Process data
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '[{"text": "Great product!", "rating": 9.0}]'

# Retrieve data (with authentication)
curl -H "api-key: your-api-key-here" \
  "http://localhost:8000/retrieve?page=1&per_page=5"
```

## 📝 Development

The project structure supports modular development:

- Add new services in `app/service/`
- Create new API routes in `app/api/routes/`
- Extend models in `app/models/`
- Add validation utilities in `app/utils/validation/`



## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs in `storage/<logid>.log`
3. Verify environment configuration
4. Ensure all dependencies are installed

---
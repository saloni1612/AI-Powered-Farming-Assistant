

# Krishi Sakhi – AI-Powered Farming Assistant

Krishi Sakhi is an AI-based agricultural advisory assistant that provides personalized, context-aware guidance to farmers using their actual farm data. Built with **FastAPI**, **LangChain**, and **Google Gemini**, it leverages a **Retrieval-Augmented Generation (RAG)** approach to deliver accurate, actionable insights.

---

## Features

- **Personalized Advisory**: Generates farmer-specific advice instead of generic guidance.  
- **RAG-based Architecture**: Combines retrieval and generative AI for precise responses.  
- **Vector Search with FAISS**: Retrieves relevant farm data from embeddings using SentenceTransformers.  
- **FastAPI Backend**: RESTful API endpoint for seamless integration.  
- **Environment-Aware Setup**: Secure API key management using `.env` files.

---

## How It Works

1. Farmer data (profile, farm details, activities, reminders) is converted to JSON context.  
2. The context is split into chunks and embedded using **SentenceTransformers**.  
3. A **FAISS** vector index is built to retrieve the most relevant chunks for a farmer's query.  
4. A **ChatGoogleGenerativeAI (Gemini 2.5 Pro)** model generates a friendly, actionable advisory based on the retrieved context.  
5. The advisory is returned via a REST API endpoint.

---

## API Endpoint

**POST** `/get-advisory`  

**Request Body Example:**
```json
{
  "farmer_data": {
    "farmer": {
      "name": "Priya Verma",
      "phoneNumber": "9988776655",
      "location": "Pune, Maharashtra"
    },
    "farms": [
      {
        "sizeInAcres": 7.8,
        "soilType": "Sandy",
        "irrigation": "Sprinkler",
        "crops": ["Rice", "Vegetables"]
      }
    ],
    "reminders": [
      {
        "message": "Schedule pest control treatment next week",
        "dueDate": "2025-09-18T09:30:00.000Z"
      }
    ]
  },
  "question": "What should I do about spraying on my brinjal crop?"
}
````

**Response Example:**

```json
{
  "advisory": "Hello! Happy to help with your brinjal crop in Pune. Inspect your plants for common issues like Fruit and Shoot Borer or Powdery Mildew. Spray early morning or late evening, avoiding windy or rainy days, and cover the undersides of leaves."
}
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/saloni1612/AI-Assistant-For-Kerela-Farmers.git
cd AI-Assistant-For-Kerela-Farmers
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your `.env` file with:

```
GOOGLE_API_KEY=your_google_api_key_here
```

4. Run the FastAPI server:

```bash
uvicorn app:app --reload
```

---

## Usage

Send a POST request to `/get-advisory` with your farmer data and question. The system will respond with personalized advisory for your crops.

---

## Technology Stack

* **FastAPI** – REST API backend
* **LangChain** – LLM orchestration
* **Google Gemini 2.5 Pro** – Generative AI model
* **FAISS** – Vector similarity search
* **SentenceTransformers** – Embedding generation

---

## Future Improvements

* Multi-language support (Malayalam, Hindi, etc.)
* Voice-based conversational interface
* Integration with real-time weather and market data

```


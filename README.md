# ViewStats

## Project Overview

ViewStats is a containerized web service designed to process CSV files and interact with a vector database (Qdrant). The backend is built with FastAPI and is orchestrated using Docker Compose for easy deployment and scalability.

---

## Project Structure

```
viewstats/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       └── services/
│           └── file_processor.py
├── docker-compose.yaml
```

### Root Directory
- **docker-compose.yaml**: Defines and orchestrates the services required for the project, including the API backend and the Qdrant vector database. It sets up networking, persistent volumes, and environment variables for service communication.

### backend/
- **Dockerfile**: Builds the backend API image using Python 3.11-slim, installs dependencies, and sets up the FastAPI application to run with Uvicorn.
- **requirements.txt**: Lists the Python dependencies for the backend (`fastapi`, `uvicorn`).
- **app/**: Contains the FastAPI application code and related services.

### backend/app/
- **main.py**: Entry point for the FastAPI application. It exposes two endpoints:
  - `GET /`: Health check endpoint returning a welcome message.
  - `POST /upload-csv`: Accepts a CSV file upload, validates the file type, processes the file, and returns the number of rows and column names. Utilizes the `file_processor` service for CSV parsing.
- **services/**: Contains auxiliary services used by the application.

### backend/app/services/
- **file_processor.py**: Implements the logic for processing CSV files. It reads the uploaded file using pandas, extracts the number of rows and column names, and returns this information to the API.

---

## How It Works

1. **Startup**: Use Docker Compose to start both the Qdrant vector database and the FastAPI backend.
2. **API Usage**:
   - Access the root endpoint (`/`) to verify the API is running.
   - Use the `/upload-csv` endpoint to upload a CSV file. The API will respond with the file's metadata (number of rows and columns).
3. **Qdrant Integration**: The backend is pre-configured to connect to the Qdrant service, though the current implementation focuses on CSV processing.

---

## Running the Project

1. **Build and Start Services**
   ```bash
   docker-compose up --build
   ```
2. **Access the API**
   - The API will be available at `http://localhost:8000`.
   - The Qdrant database will be available at `http://localhost:6333`.

---

## Dependencies
- Python 3.11 (Dockerized)
- FastAPI
- Uvicorn
- pandas (for CSV processing, assumed to be available in the runtime)
- Qdrant (vector database)

---

## Extending the Project
- Add more endpoints to process or analyze uploaded data.
- Integrate deeper with Qdrant for vector search or storage.
- Implement authentication and authorization for secure file uploads.

---

## License
This project is provided as-is for demonstration and educational purposes. 
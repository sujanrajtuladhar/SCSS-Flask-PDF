# PDF Parsing API

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
   - [Manual Setup](#manual-setup)
   - [Docker Setup](#docker-setup)
5. [Running Tests](#running-tests)
   - [Manual Setup Tests](#manual-setup-tests)
   - [Docker Tests](#docker-tests)
6. [Test Data](#test-data)
7. [API Endpoints](#api-endpoints)
   - [Upload PDF for Parsing](#1-upload-pdf-for-parsing)
   - [Check Task Status](#2-check-task-status)
8. [Explanation of Functions](#explanation-of-functions)
9. [File Structure](#file-structure)
10. [Postman Collection](#postman-collection)

---

## Overview

This project provides a RESTful API built with Flask for parsing tables from PDF files and saving them to CSV format. The API utilizes Celery for background task processing, enabling asynchronous handling of PDF parsing tasks.

---

## Features

- Upload PDF files and parse tables from them.  
- Save extracted tables as CSV files.  
- Asynchronous processing of PDF parsing tasks using Celery.  
- Check the status of parsing tasks and download results.  

---

## Prerequisites

- [Docker](https://www.docker.com/)  
- [Flask](https://flask.palletsprojects.com/en/stable/)  
- [Python 3.10+](https://www.python.org/downloads/release/python-3100/)  
- [Redis](https://redis.io/)  

---

## Installation

### Manual Setup

Follow these steps to set up the application without Docker:  

1. **Clone the repository:**  

   ```bash
   git clone git@github.com:sujanrajtuladhar/SCSS-Flask-PDF.git
   cd SCSS-Flask-PDF
   ```

2. **Set up a virtual environment:**  

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**  

   ```bash
   pip install -r requirements.txt
   ```

4. **Start Redis (required for Celery):**  

   ```bash
   redis-server
   ```

5. **Run Celery worker:**  

   ```bash
   celery -A tasks worker --loglevel=info
   ```

6. **Run the Flask application:**  

   ```bash
   python3 app.py
   ```

The application will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).  

---

### Docker Setup

If you prefer using Docker, follow these steps:  

1. **Clone the repository:**  

   ```bash
   git clone git@github.com:sujanrajtuladhar/SCSS-Flask-PDF.git
   cd SCSS-Flask-PDF
   ```

2. **Build and start the containers:**  

   ```bash
   docker-compose up --build
   ```

   This will set up the following services:  
   - Flask application  
   - Celery worker  
   - Redis (as the Celery broker)  

3. **Access the application:**  
   The application will be available at [http://localhost:5000](http://localhost:5000).

---

## Running Tests

### Manual Setup Tests  

Run the unit tests manually for different components:  

1. **Run Flask app(api) tests:**  

   ```bash
   python3 -m unittest server/tests/test_app.py
   ```

2. **Run PDF parser tests:**  

   ```bash
   python3 -m unittest server/tests/test_pdf_parser.py
   ```

### Docker Tests  

If using Docker, execute the tests within the Docker container:  

```bash
docker compose exec web pytest
```  

---

## Test Data

Sample PDFs for testing are available in the test_data folder within the server/tests directory. These include:

- [sample_empty_pdf.pdf](server/tests/test_data/sample_empty_pdf.pdf): A PDF file with no content.
- [sample_with_tables.pdf](server/tests/test_data/sample_with_tables.pdf): A PDF file containing tables.
- [sample_without_tables.pdf](server/tests/test_data/sample_without_tables.pdf): A PDF file without tables.

These files are used for validating the parsing functionality of the API.

---

## API Endpoints

### 1. **Upload PDF for Parsing**  

   **Endpoint:** `/upload`  
   **Method:** `POST`  
   **Description:** Upload a PDF file to parse tables.  

   Example:  

   ```bash
   curl -X POST -F "file=@sample.pdf" http://localhost:5000/upload
   ```

### 2. **Check Task Status**  

   **Endpoint:** `/status/<task_id>`  
   **Method:** `GET`  
   **Description:** Check the status of a parsing task.  

   Example:  

   ```bash
   curl -X GET http://localhost:5000/status/<task_id>
   ```

---

## Explanation of Functions

For detailed explanations of each function used across the project, check out the [Functions Explanation Document](docs/explanation/functions_explanation.md)

---

## File Structure

```plaintext
SCSS-Flask-PDF/
├─ .docker/
│  └─ Dockerfile
├─ .gitignore
├─ README.md
├─ app.py
├─ docker-compose.yml
├─ requirements.txt
├─ doc/
│  └─ postman_collection/
│     └─ SCSS.postman_collection.json
├─ server/
│  ├─ __init__.py
│  ├─ celeryconfig.py
│  ├─ pdf_parser.py
│  ├─ routes.py
│  ├─ tasks.py
│  └─ tests/
│     ├─ __init__.py
│     ├─ test_app.py
│     ├─ test_data/
│     │  ├─ sample_empty_pdf.pdf
│     │  ├─ sample_with_tables.pdf
│     │  └─ sample_without_tables.pdf
│     └─ test_pdf_parser.py
└─ static/
```

---

## Postman Collection

For testing the API endpoints, a Postman collection is provided in the docs/postman_collection/ directory:

- [SCSS.postman_collection.json](docs/postman_collection/SCSS.postman_collection.json): This JSON file contains all the API endpoints and their corresponding requests

```plaintext
# To import into Postman:
1. Open Postman
2. Go to File -> Import
3. Select the `SCSS.postman_collection.json` file
```

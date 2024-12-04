# PDF Parsing API

## Overview

This project provides a RESTful API built with Flask for parsing tables from PDF files and saving them to CSV format. The API utilizes Celery for background task processing, allowing for asynchronous handling of PDF parsing tasks.

## Features

- Upload PDF files and parse tables from them.
- Save extracted tables as CSV files.
- Asynchronous processing of PDF parsing tasks using Celery.
- Check the status of parsing tasks and download results.

## Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) If using Docker, build and run the containers:

   ```bash
   docker-compose up --build
   ```

## Usage

### Running the Application

To run the application locally, execute:

   ```bash
   python app.py
   ```

The API will be available at http://127.0.0.1:5000.

python3 -m unittest test_app.py
python3 -m unittest test_celery.py
docker compose exec web pytest
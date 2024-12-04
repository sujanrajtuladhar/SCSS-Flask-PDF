import pytest
import os
import logging
from flask import Flask

# Import your app from app.py
from app import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup test fixtures
@pytest.fixture
def client():
    """Flask test client fixture."""
    with app.test_client() as client:
        yield client

@pytest.fixture
def pdf_file(tmp_path):
    """Fixture to create a temporary PDF file."""
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_text("Sample PDF content")
    return str(pdf_path)

# Test cases
def test_upload_pdf_valid_file(client, pdf_file):
    """Test uploading a valid PDF file."""
    logger.info("Running test: test_upload_pdf_valid_file")
    with open(pdf_file, 'rb') as f:
        data = {'file': (f, 'test.pdf')}
        response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 202
    assert 'id' in response.json
    logger.info("Test passed: test_upload_pdf_valid_file")

def test_upload_pdf_no_file(client):
    """Test uploading without a file."""
    logger.info("Running test: test_upload_pdf_no_file")
    response = client.post('/upload', content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.json['error'] == 'No file part'
    logger.info("Test passed: test_upload_pdf_no_file")

def test_upload_pdf_empty_file(client):
    """Test uploading an empty file."""
    logger.info("Running test: test_upload_pdf_empty_file")
    data = {'file': (b'', '')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.json['error'] == 'No selected file'
    logger.info("Test passed: test_upload_pdf_empty_file")

def test_status_not_found(client):
    """Test checking the status of a non-existent task."""
    logger.info("Running test: test_status_not_found")
    response = client.get('/status/invalid_task_id')
    assert response.status_code == 404
    assert response.json['error'] == 'Task ID not found'
    logger.info("Test passed: test_status_not_found")

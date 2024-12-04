import os
import logging
import tabula
import pandas as pd

from celery import Celery

from pdf_parser import parse_pdf

app = Celery('tasks')
app.config_from_object('celeryconfig')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task
def parse_pdf_task(file_path, output_folder):
    """
    Task to parse a PDF file, extract table content, and save the output as a CSV.

    :param file_path: The path to the PDF file to be parsed
    :type file_path: str
    :param output_folder: The folder where the output CSV will be saved
    :type output_folder: str
    """
    try:
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Generate unique output file names
        csv_path = os.path.join(output_folder, f'output.csv')
        error_path = os.path.join(output_folder, f'error.txt')
        
        # Call the parse_pdf function to parse the PDF
        parse_pdf(file_path, csv_path, error_path)

    except Exception as e:
        # Log and write the error to a file
        logger.error(f"Error while parsing PDF: {e}")
        with open(error_path, 'w') as f:
            f.write(f"Error: {e}\n")

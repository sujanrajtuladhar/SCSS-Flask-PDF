import os
import pytest
import pandas as pd

from server.pdf_parser import parse_pdf


@pytest.fixture
def temp_dir(tmp_path):
    """
    Fixture to provide a temporary directory for test files.
    """
    return tmp_path


@pytest.fixture
def tests_dir():
    """
    Fixture to provide the path to the tests folder containing test PDF files.
    """
    return os.path.join(os.path.dirname(__file__), 'test_data')


def test_parse_pdf_with_tables(temp_dir, tests_dir):
    """
    Test parsing a PDF with tables.
    """
    pdf_path = os.path.join(tests_dir, "sample_with_tables.pdf")
    csv_path = os.path.join(temp_dir, "output.csv")
    error_path = os.path.join(temp_dir, "error.txt")

    # Run the parser
    parse_pdf(pdf_path, csv_path, error_path)

    # Assert that the CSV file is created and contains data
    assert os.path.exists(csv_path), "CSV file was not created."
    output_df = pd.read_csv(csv_path)
    assert not output_df.empty, "CSV file is empty."
    assert list(output_df.columns) == ['User', 'Email', 'Role', 'Token', 'Type', 'Expiring'], "CSV columns do not match expected columns."

    # Assert that the error file is not created
    assert not os.path.exists(error_path), "Error file should not be created for PDFs with tables."


def test_parse_pdf_without_tables(temp_dir, tests_dir):
    """
    Test parsing a PDF without tables.
    """
    pdf_path = os.path.join(tests_dir, "sample_without_tables.pdf")
    csv_path = os.path.join(temp_dir, "output.csv")
    error_path = os.path.join(temp_dir, "error.txt")

    # Run the parser
    parse_pdf(pdf_path, csv_path, error_path)

    # Assert that the CSV file is not created
    assert not os.path.exists(csv_path), "CSV file should not be created for PDFs without tables."

    # Assert that the error file is created and contains the correct message
    assert os.path.exists(error_path), "Error file was not created."
    with open(error_path, 'r') as f:
        error_message = f.read()
    assert "No tables found in the PDF" in error_message, "Error message does not match expected message."


def test_parse_pdf_invalid_path(temp_dir):
    """
    Test parsing with an invalid PDF file path.
    """
    invalid_pdf_path = os.path.join(temp_dir, "non_existent_file.pdf")
    csv_path = os.path.join(temp_dir, "output.csv")
    error_path = os.path.join(temp_dir, "error.txt")

    # Run the parser with a non-existent file
    with pytest.raises(Exception) as excinfo:
        parse_pdf(invalid_pdf_path, csv_path, error_path)

    # Assert that an exception is raised
    assert "No such file or directory" in str(excinfo.value), "Expected file not found error."


def test_parse_pdf_empty_pdf(temp_dir, tests_dir):
    """
    Test parsing an empty PDF file.
    """
    empty_pdf_path = os.path.join(tests_dir, "sample_empty_pdf.pdf")
    csv_path = os.path.join(temp_dir, "output.csv")
    error_path = os.path.join(temp_dir, "error.txt")

    # Run the parser
    parse_pdf(empty_pdf_path, csv_path, error_path)

    # Assert that the CSV file is not created
    assert not os.path.exists(csv_path), "CSV file should not be created for an empty PDF."

    # Assert that the error file is created
    assert os.path.exists(error_path), "Error file was not created."
    with open(error_path, 'r') as f:
        error_message = f.read()
    assert "No tables found in the PDF" in error_message, "Error message does not match expected message."

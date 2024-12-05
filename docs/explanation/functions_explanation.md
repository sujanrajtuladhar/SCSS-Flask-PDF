# Functions Explanation

This document provides explanations for the key functions used across the project. Each function's purpose, parameters, and usage are described to provide a clear understanding of how they work.

## Table of Contents

1. [App Setup](#app-setup)
2. [Celery Tasks](#celery-tasks)
3. [PDF Parsing](#pdf-parsing)
4. [Routes](#routes)

---

## App Setup

### `create_app()`

- **Location:** `app.py`
- **Purpose:** Creates and configures the Flask application instance.
- **Parameters:** None
- **Returns:** Flask app instance
- **Explanation:** This function sets up the Flask application, configures the upload folder, and registers routes. It is called when the app starts.

```python
def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask app instance.
    """
    app = Flask(__name__)
    
    # Create upload folder
    app.config['UPLOAD_FOLDER'] = 'static'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register routes
    register_routes(app)
    
    return app
```

---

## Celery Tasks

### `parse_pdf_task(file_path, output_folder)`

- **Location:** `server/tasks.py`
- **Purpose:** A Celery task that parses a PDF file, extracts table content, and saves the output as a CSV.
- **Parameters:**
  - `file_path`: Path to the PDF file to parse
  - `output_folder`: Folder where the parsed CSV will be saved
- **Returns:** None
- **Explanation:** This task ensures the output folder exists, generates unique output file names, calls the `parse_pdf` function to parse the PDF, and logs any errors that occur during parsing.

```python
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
```

---

## PDF Parsing

### `parse_pdf(file_path, csv_path, error_path)`

- **Location:** `server/pdf_parser.py`
- **Purpose:** A function that parses a PDF file to extract tables and save them as a CSV file.
- **Parameters:**
  - `file_path`: The path to the PDF file to be parsed.
  - `csv_path`: The path where the resulting CSV file will be saved.
  - `error_path`: The path where an error message will be written if no tables are found.
- **Returns:** None
- **Explanation:** This function uses the tabula library to read all tables from the specified PDF file, combines the tables into a single DataFrame, standardizes the columns to match the structure of the first table, and saves the combined DataFrame to the specified CSV file path. If no tables are found in the PDF, an error message is written to the specified error file path.

```python
def parse_pdf(file_path, csv_path, error_path):
    """
    Parses a PDF file to extract tables and save them as a CSV file.

    This function uses the tabula library to read all tables from the specified
    PDF file. It combines the tables into a single DataFrame, standardizing the
    columns to match the structure of the first table. The combined DataFrame
    is then saved to the specified CSV file path. If no tables are found in the
    PDF, an error message is written to the specified error file path.

    Args:
        file_path (str): The path to the PDF file to be parsed.
        csv_path (str): The path where the resulting CSV file will be saved.
        error_path (str): The path where an error message will be written if no tables are found.

    Returns:
        None
    """
    logger.info(f"Starting PDF parsing for {file_path}")
            
    # Extract tables from PDF using tabula
    # Read all tables from the PDF
    tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True, lattice=True)

    # Check if no tables or all tables are empty
    if not tables or all(table.empty for table in tables):
        logger.warning("No tables found in the PDF.")
        with open(error_path, 'w') as error_file:
            error_file.write("No tables found in the PDF.")
        return
        
    if tables:
        logger.info('table exists')
        logger.info(f"Found {len(tables)} table(s) in the PDF.")
        combined_df = pd.DataFrame()  # Initialize an empty DataFrame for combining tables

        for i, table in enumerate(tables):
            if table.empty:
                continue  # Skip empty tables

            # Standardize the columns to match the first table's structure
            if combined_df.empty:
                combined_df = table  # Use the first table's structure as a reference
            else:
                table.columns = combined_df.columns[:len(table.columns)]
                combined_df = pd.concat([combined_df, table], ignore_index=True)

        # Save the combined DataFrame to a single CSV file
        combined_df.to_csv(csv_path, index=False)
        
        logger.info(f"PDF parsing completed. Output saved to {csv_path}")
    else:
        logger.info('table doesnt exists')
        logger.warning(f"No tables found in the PDF {file_path}")
        with open(error_path, 'w') as f:
            f.write(f"No tables found in the PDF {file_path}\n")
```

---

## Routes

### `register_routes(app)`

- **Location:** `server/routes.py`
- **Purpose:** Registers all routes for the Flask app.
- **Parameters:**
  - `app`: The Flask app instance.
- **Returns:** None
- **Explanation:** This function defines all routes and their associated view functions for the application.

### `upload_pdf()`

- **Location:** `server/routes.py`
- **Purpose:** Handles file upload and initiates a background task to parse the uploaded PDF.
- **Parameters:** None
- **Returns:** A JSON response containing a unique ID for the task if the file is uploaded successfully, or an error message if no file is provided or selected.
- **Explanation:** This function defines the view for the `/upload` route, handling POST requests with a PDF file. It saves the file to a unique directory, triggers a background task to parse the PDF using Celery, and returns a JSON response with a unique task ID.

```python
def upload_pdf():
    """
    Handle file upload and initiate a background task to parse the uploaded PDF.

    This endpoint accepts a POST request with a PDF file. It saves the file to a
    unique directory within the static folder, and then triggers a background task
    to parse the PDF and extract tables. The task runs asynchronously using Celery.

    Returns:
        A JSON response containing a unique ID for the task if the file is uploaded
        successfully, with a status code of 202. If no file is provided or no file
        is selected, returns an error message with a status code of 400.

    :param file: The uploaded PDF file
    :type file: werkzeug.datastructures.FileStorage
    :return: A JSON response with a unique ID for the task
    :rtype: flask.Response
    """
    if 'file' not in request.files:
        # No file was provided
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        # No file was selected
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Generate a unique ID for the task
        unique_id = str(uuid.uuid4())
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_id)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file.filename)
        file.save(file_path)

        # Trigger background task to parse the PDF
        parse_pdf_task.delay(file_path, folder_path)

        # Return a JSON response with the task ID
        return jsonify({'id': unique_id}), 202
```

### `check_status(task_id)`

- **Location:** `server/routes.py`
- **Purpose:** Checks the status of a task with the given task ID and returns the result.
- **Parameters:**
  - `task_id`: The ID of the task to check the status for.
- **Returns:**
  - A JSON response with a status code of 404 if the task ID is not found.
  - A JSON response with a status code of 200 if the task is in progress.
  - The output CSV file if the task is complete.
  - The output error text file if the task encountered an error.
- **Explanation:** This function defines the view for the `/status/<task_id>` route, handling GET requests to check the status of a task. It checks the existence of a folder with the task ID, looks for output files (CSV or TXT), and returns the corresponding response based on the task status.

```python
def check_status(task_id):
    """
    GET Endpoint to check the status of a task and download the output.

    Returns:
        - A JSON response with a status code of 404 if the task ID is not found
        - A JSON response with a status code of 200 if the task is in progress
        - The output CSV file if the task is complete
        - The output error text file if the task encountered an error
    """
    # Get the folder path for the task
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], task_id)

    # Check if the task ID exists
    if not os.path.exists(folder_path):
        # Return a JSON response with a status code of 404 if the task ID is not found
        return jsonify({'error': 'Task ID not found'}), 404

    # Check for Outputs
    csv_file = next((f for f in os.listdir(folder_path) if f.endswith('.csv')), None)
    txt_file = next((f for f in os.listdir(folder_path) if f.endswith('.txt')), None)

    # Return the output CSV file if the task is complete
    if csv_file:
        return send_from_directory(folder_path, csv_file)
    # Return the output error text file if the task encountered an error
    elif txt_file:
        return send_from_directory(folder_path, txt_file)
    else:
        # Return a JSON response with a status code of 200 if the task is in progress
        return jsonify({'status': 'in-progress'}), 200
```

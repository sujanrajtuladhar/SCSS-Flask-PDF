import os
import uuid
from flask import request, jsonify, send_from_directory
from server.tasks import parse_pdf_task


def register_routes(app):
    """
    Register all the application routes.

    Args:
        app (Flask): The Flask application instance.
    """

    # POST Endpoint
    @app.route('/upload', methods=['POST'])
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

    # GET Endpoint
    @app.route('/status/<task_id>', methods=['GET'])
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
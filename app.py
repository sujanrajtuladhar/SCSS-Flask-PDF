import os
from flask import Flask
from server.routes import register_routes

# Application Factory
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


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

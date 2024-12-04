FROM python:3.10-slim

# Install dependencies
# Update package lists and install dependencies for tabula-py (Java is required for tabula-py)
RUN apt-get update && apt-get install -y \
    default-jre \
    # Install other dependencies if required
    && rm -rf /var/lib/apt/lists/*

# Verify Java installation (optional)
RUN java -version

# Verify Java installation
RUN java -version

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]

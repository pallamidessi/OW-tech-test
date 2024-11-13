PORT = 5000
IMAGE_NAME = flask_app
CONTAINER_NAME = flask_app_container

.PHONY: run setup test clean build

# Install dependencies
setup:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Build Docker image
build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME) .

# Run the Flask application in Docker
run: build
	@echo "Running Flask application in Docker..."
	docker run -t -p $(PORT):$(PORT) $(IMAGE_NAME)

# Run tests
test:
	@echo "Running tests..."
	docker run --rm $(IMAGE_NAME) pytest tests

# Clean up .pyc and __pycache__
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r {} +


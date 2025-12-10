.PHONY: help install run docker-build docker-run docker-stop clean test

help:
	@echo "dPro QA Assistant - Make Commands"
	@echo ""
	@echo "  make install       - Install Python dependencies"
	@echo "  make run          - Run the application locally"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run with Docker Compose"
	@echo "  make docker-stop  - Stop Docker containers"
	@echo "  make clean        - Clean generated files"
	@echo "  make test         - Test the application"

install:
	pip install -r requirements.txt

run:
	@mkdir -p static
	@cp index.html static/
	@cp style.css static/ 2>/dev/null || true
	python app.py

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

clean:
	rm -rf __pycache__ *.pyc static/ test_venv/ venv/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

test:
	@echo "Testing Flask app startup..."
	@mkdir -p static
	@cp index.html static/
	@cp style.css static/ 2>/dev/null || true
	@echo "Starting app for 10 seconds..."
	@timeout 10 python app.py || true
	@echo "Test completed!"

#!/bin/bash

echo "=== dPro Deployment Test Suite ==="
echo ""

# Test 1: Check required files exist
echo "Test 1: Checking required files..."
required_files=("app.py" "index.html" "requirements.txt" "Dockerfile" "docker-compose.yml" "run.sh" "README.md" "README_DEPLOY.md" "Makefile")
all_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
        all_exist=false
    fi
done

if [ "$all_exist" = true ]; then
    echo "  ✓ All required files present"
else
    echo "  ✗ Some files missing"
    exit 1
fi

echo ""

# Test 2: Check Python syntax
echo "Test 2: Checking Python syntax..."
if python3 -m py_compile app.py 2>/dev/null; then
    echo "  ✓ app.py syntax valid"
else
    echo "  ✗ app.py syntax error"
    exit 1
fi

echo ""

# Test 3: Check requirements.txt format
echo "Test 3: Checking requirements.txt..."
if grep -q "Flask" requirements.txt && grep -q "gunicorn" requirements.txt; then
    echo "  ✓ requirements.txt contains necessary packages"
else
    echo "  ✗ requirements.txt incomplete"
    exit 1
fi

echo ""

# Test 4: Check Dockerfile syntax
echo "Test 4: Checking Dockerfile..."
if grep -q "FROM python" Dockerfile && grep -q "EXPOSE 5000" Dockerfile; then
    echo "  ✓ Dockerfile properly configured"
else
    echo "  ✗ Dockerfile configuration issue"
    exit 1
fi

echo ""

# Test 5: Check run.sh is executable
echo "Test 5: Checking run.sh permissions..."
if [ -x "run.sh" ]; then
    echo "  ✓ run.sh is executable"
else
    echo "  ✗ run.sh not executable"
    chmod +x run.sh
    echo "  ✓ Fixed: run.sh is now executable"
fi

echo ""

# Test 6: Check Makefile targets
echo "Test 6: Checking Makefile..."
if grep -q "^run:" Makefile && grep -q "^docker-build:" Makefile; then
    echo "  ✓ Makefile contains required targets"
else
    echo "  ✗ Makefile incomplete"
    exit 1
fi

echo ""

echo "=== All Tests Passed! ==="
echo "The application is ready to deploy and run."
echo ""
echo "Quick start options:"
echo "  1. ./run.sh"
echo "  2. make run"
echo "  3. docker-compose up --build"

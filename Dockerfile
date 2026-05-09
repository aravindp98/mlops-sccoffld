# Step 1: Use a modern Python version
FROM python:3.13-slim

# Step 2: Set the home for our code
WORKDIR /app

# Step 3: Copy everything from your D: drive into the container
COPY . /app

# Step 4: Install libraries directly
RUN pip install --no-cache-dir -r requirement.txt

# Step 5: Run the tests to prove the container is "healthy"
# CMD ["python", "-m", "pytest", "-vv", "test_main.py"]
CMD ["python",  "main.py"]
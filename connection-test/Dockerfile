FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test script
COPY test_connection.py .

# Run the test (keeps container alive by sleeping after test)
CMD python test_connection.py && echo "\n✅ Test complete. Sleeping..." && sleep infinity

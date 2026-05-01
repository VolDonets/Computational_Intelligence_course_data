FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src folder into the container
COPY ./src /app/src

# Expose the Streamlit web port
EXPOSE 8501

# Run the app from inside the src directory
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
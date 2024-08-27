# Base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files
COPY main.py /app/
COPY streamlit.py /app/

# Expose the Streamlit port
EXPOSE 8501

# Default command to run Streamlit
CMD ["streamlit", "run", "streamlit.py"]

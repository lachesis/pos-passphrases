# Use an official Python runtime as the base image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install NLTK library and dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download WordNet data using NLTK
RUN python -c "import nltk; nltk.download('wordnet')"

# Copy the rest of the application code to the container
COPY . .

# Set the command to run the application
CMD [ "python", "dump.py" ]

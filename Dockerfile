# Base Image
FROM python:3.12

# Working Directory
WORKDIR /app

# Copy files to app dir
COPY . /app

# Run Command
RUN pip install -r requirements.txt

# Port
EXPOSE 8501

# Commans to run the code
CMD [ "streamlit" , "run", "main.py"]

FROM python:3.7.3-stretch

# Working Directory
WORKDIR /api

# Copy source code to working directory
COPY . api.py /api/

# Install packages from requirements.txt
RUN pip3 install -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Run api.py at container launch
ENTRYPOINT ["python", "api.py"]
FROM python:3.7.3-stretch

# Working Directory
WORKDIR /api

# Copy source code to working directory
COPY . api.py /api/

# Install packages from requirements.txt
RUN pip3 install -r requirements.txt

# Install Google SDK
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin

# Expose port 8080
EXPOSE 8080

# Run api.py at container launch
CMD ["/bin/bash", "run_api.sh"]
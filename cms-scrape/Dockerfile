FROM ubuntu:18.04

# Install Python and Linux tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    vim \
    unzip \
    tmux

# Install Python packages
RUN pip3 install pandas && \
    pip3 install numpy && \
    pip3 install flask && \
    pip3 install requests && \
    pip3 install google-cloud-storage && \
    pip3 install zipfile36 && \
    pip3 install bs4 && \
    pip3 install waitress && \
    pip3 install pyarrow

# Copy source code
COPY . main.py /processing/

# Working Directory
WORKDIR processing

# Update and make directory for processing files
RUN apt-get update && \
    apt-get install sudo -y && \
    cd /processing && \ 
    mkdir files && \
    rm -r /root/.cache/pip

# Add scraping file and logging
ADD scraper.py /processing/scraper.py
ADD scrape.log /processing/scrape.log

# Expose port 80
EXPOSE 80

# Run main.py at container launch
CMD ["python3", "main.py"]
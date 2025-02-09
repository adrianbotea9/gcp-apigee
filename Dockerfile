FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

#copy requirments first be more eficient
COPY requirments.txt .
RUN pip3 install --no-cache-dir -r requirments.txt
#in case the app code changes, docker can reuse above layers from cache and not install reqs again
# copy app code and init script
COPY gcp/ ./gcp/
COPY init.sh .

#make init script executable
RUN chmod +x init.sh

#set init script as the default command
ENTRYPOINT ["./init.sh"]
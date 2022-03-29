FROM fedora:latest

RUN dnf install -y python3-pip && dnf clean all

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt && \
    python3 setup.py install

CMD ["/usr/local/bin/ecasbot"]

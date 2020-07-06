FROM registry.fedoraproject.org/fedora:32

RUN dnf install -y python3-pip && dnf clean all

COPY . .
RUN pip3 install -r requirements.txt && \
    python3 setup.py install

CMD ["/usr/local/bin/ecasbot"]

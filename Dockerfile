# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

FROM fedora:35

RUN dnf install -y python3-pip && dnf clean all

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt && \
    python3 setup.py install

CMD ["/usr/local/bin/ecasbot"]

# SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

FROM fedora:38

RUN dnf install -y python3-pip && dnf clean all

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir .

CMD ["/usr/local/bin/ecasbot"]

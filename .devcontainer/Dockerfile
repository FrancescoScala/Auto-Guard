# Copyright (c) 2024 Elektrobit Automotive GmbH and others

# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# SPDX-License-Identifier: Apache-2.0

FROM ghcr.io/eclipse-ankaios/app-ankaios-dev:0.4.1 AS dev
ARG TARGETARCH

RUN apt-get update && apt-get -y install \
    git \
    jq \
    python3 \
    python3-pip \
    # eCAL dependencies
    libc6 \
    libcurl4 \
    libgcc-s1 \
    libhdf5-103 \
    libprotobuf23 \
    libqt5core5a \
    libqt5gui5 \
    libqt5widgets5 \
    libqt5svg5 \
    libstdc++6 \
    sysstat \
    ifstat \
    libqwt-qt5-6 \
    libyaml-cpp0.7 \
    # Add your development tools here ...
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && curl -sL https://github.com/mikefarah/yq/releases/latest/download/yq_linux_${TARGETARCH} -o /usr/bin/yq \
    && chmod +x /usr/bin/yq

# install eCAL
RUN curl -sL https://github.com/eclipse-ecal/ecal/releases/download/v5.11.3/ecal_5.11.3-jammy_amd64.deb -o /tmp/ecal.dep \
    && dpkg -i /tmp/ecal.dep \
    && curl -sL https://github.com/eclipse-ecal/ecal/releases/download/v5.11.3/ecal5-5.11.3-1jammy-cp310-cp310-linux_x86_64.whl -o /tmp/ecal5-5.11.3-1jammy-cp310-cp310-linux_x86_64.whl \
    && pip3 install --no-cache-dir /tmp/ecal5-5.11.3-1jammy-cp310-cp310-linux_x86_64.whl \
    # Cleanup
    && rm -rf /tmp/ecal.dep /tmp/ecal5-5.11.3-1jammy-cp310-cp310-linux_x86_64.whl

# Trust all repositories in this container
RUN git config --global --add safe.directory '*' \
    && echo "if [ -f /etc/bash_completion ] && ! shopt -oq posix; then\n . /etc/bash_completion \nfi" >> /root/.bashrc
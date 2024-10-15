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

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    software-properties-common \
    git \
    jq \
    python3 \
    python3-pip \
    # Add your development tools here ...
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && curl -sL https://github.com/mikefarah/yq/releases/latest/download/yq_linux_${TARGETARCH} -o /usr/bin/yq \
    && chmod +x /usr/bin/yq \
    # install eCAL
    && add-apt-repository ppa:ecal/ecal-5.12 \
    && apt-get install -y python3-ecal5

# Trust all repositories in this container
RUN git config --global --add safe.directory '*' \
    && echo "if [ -f /etc/bash_completion ] && ! shopt -oq posix; then\n . /etc/bash_completion \nfi" >> /root/.bashrc
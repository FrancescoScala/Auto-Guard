# Forget the conventional - Shift to SDV

This repository provides a starter template for solving the Forget the conventional - Shift to SDV challenge using the [Ankaios](https://github.com/eclipse-ankaios/ankaios) workload orchestrator.

It contains a pre-configured devcontainer that makes it easy for you to start developing and building container applications managed by Ankaios.

The container is designed to have an immediately running environment combined with a development environment for Ankaios workloads. Once triggered, all workloads are initially started and sample data is output.

## Links

- [Ankaios docs](https://eclipse-ankaios.github.io/ankaios/0.5/)
- [Ankaios Dashboard](https://github.com/FelixMoelders/ankaios-dashboard)
- [Ankaios quickstart](https://eclipse-ankaios.github.io/ankaios/0.5/usage/quickstart/)
- [eCAL docs](https://eclipse-ecal.github.io/ecal/)
- [Symphony docs](https://github.com/eclipse-symphony/symphony/tree/main/docs)
- [Podman](https://docs.podman.io/en/v4.9.3/)
- [What are devcontainers?](https://containers.dev/)

# Challenge

The challenge is to turn an ordinary vehicle into an innovation platform. To achive this two paths are available to the participants: the "Feature Path" and the "Connectivity Path". Both paths have different targets, yet combined showcase what a full-blown software-defined vehicle is capable of.

The following diagram shows the context view of the two paths:

![Context View](diagrams/context.drawio.svg)

## Feature Path

Unleash your creativity and develop innovative containerized applications managed by Ankaios using real data from the test vehicle.

Data is delivered via eCAL topics that your application subscribes to.

### GNSS

TODO

### Vehilce dynamics

TODO

### Traffic sign detection

Using the front camera of the test vehicle, an AI model predicts the class ID of traffic signs.

You can get the inference results by subscribing to the eCAL topic `traffic_sign_detection`. More infomration on the objects provided by the topic can be found [here](traffic_sign_detection.md). 

### Radar sensor data

TODO!

## Connectivity Path

Manage your fleet from the cloud turning feature upgrades into a seamless day-to-day business​.​

The connectivity path enables over-the-air updates and upgrades.

To enable this, write a Symphony provider application that receives an Ankaios manifest via the Eclipse Symphony meta-orchestrator running on Azure. The provider receives the new Ankaios manifest from the cloud and forwards the Ankaios manifest to Ankaios, which deploys all of the manifest's workloads. Workloads are updated over-the-air by simply changing the image version of the containers to point to a different version of the application.

... TODO!

## Development environment

The following is provided inside the devcontainer:

- Ankaios executables (`ank-server`, `ank-agent` and `ank`)

- Podman 4.9.3

- Pre-configured Ankaios startup config [startupState.yaml](./config/startupState.yaml)

- Automation scripts for starting and stopping all workloads of the challenge:
    - run_shift2sdv.sh (TODO! must be created)
    - shutdown_shift2sdv.sh (TODO! must be created)

- REST API providing [resource usage statistics](#resource-usage-statistics) for the sample scenario about intelligent orchestrator

- Exposed port:
    - 25551: for optionally using the Ankaios CLI outside of the devcontainer

## Run devcontainer with VSCode

### Prerequisites
- [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) extension installed in VSCode

Open the subfolder containing this README file in VSCode:

```shell
code .
```

VSCode detects automatically that a `.devcontainer` folder exists inside this subfolder.
Please confirm the dialog to reopen VSCode inside the devcontainer.
Afterwards, open a new terminal inside the devcontainer in VSCode.

## Run devcontainer without VSCode

Navigate to the subfolder containing this README file and run the following command to build the devcontainer image:

```shell
docker build -t shift2sdv-dev:0.1 --target dev -f .devcontainer/Dockerfile .
```

Start the devcontainer with the required mount points:

```shell
docker run -it --privileged --name shift2sdv-dev -v <absolute/path/to>/challenge-shift-to-sdv:/workspaces/shift2sdv -p 25551:25551 --workdir /workspaces/shift2sdv shift2sdv-dev:0.1 /bin/bash
```

## Container logs

Use the [podman logs](https://docs.podman.io/en/v4.6.1/markdown/podman-logs.1.html) command to check the logs of your container applications for debugging purposes.

```shell
podman ps -a
podman logs -f <container_name|container_id>
```

## Ankaios logs

There are log files for debugging purposes of Ankaios server and agent.

The Ankaios server logs can be viewed by executing the following command:

```shell
tail -f /var/log/ankaios-server.log
```

The Ankaios agent logs can be viewed by executing the following command:

```shell
tail -f /var/log/ankaios-agent_A.log
```


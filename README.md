# Forget the conventional - Shift to SDV

This repository provides a starter template for solving the Forget the conventional - Shift to SDV challenge using the [Ankaios](https://github.com/eclipse-ankaios/ankaios) workload orchestrator.
It contains a pre-configured devcontainer that makes it easy for you to start developing and building container applications managed by Ankaios.

The container is designed to have an immediately running environment combined with a development environment for Ankaios workloads. Once triggered, all workloads are initially started and sample data is output.

## Links

- [Ankaios docs](https://eclipse-ankaios.github.io/ankaios/0.4/)
- [Ankaios quickstart](https://eclipse-ankaios.github.io/ankaios/0.4/usage/quickstart/)
- [Podman](https://docs.podman.io/en/v4.6.1/)
- [What are devcontainers?](https://containers.dev/)

## Development environment

The following is provided inside the devcontainer:

- Ankaios executables (`ank-server`, `ank-agent` and `ank`)

- Podman 4.6.2

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


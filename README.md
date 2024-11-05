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

### Traffic sign detection

Using the front camera of the test vehicle, an AI model predicts the class ID of traffic signs.

You can get the inference results by subscribing to the eCAL topic `traffic_sign_detection_topic`.

The table below shows the supported traffic signs:

| Class ID | Label Name                            |
|----------|---------------------------------------|
|        0 | prohibitory_no_entry                  |
|        1 | prohibitory_left                      |
|        2 | prohibitory_overtake                  |
|        3 | prohibitory_right                     |
|        4 | prohibitory_speed_limit_10            |
|        5 | prohibitory_speed_limit_100           |
|        6 | prohibitory_speed_limit_130           |
|        7 | prohibitory_speed_limit_20            |
|        8 | prohibitory_speed_limit_30            |
|        9 | prohibitory_speed_limit_40            |
|       10 | prohibitory_speed_limit_5             |
|       11 | prohibitory_speed_limit_50            |
|       12 | prohibitory_speed_limit_60            |
|       13 | prohibitory_speed_limit_70            |
|       14 | prohibitory_speed_limit_80            |
|       15 | prohibitory_speed_limit_90            |
|       16 | prohibitory_stopping                  |
|       17 | prohibitory_trucks                    |
|       18 | prohibitory_u_turn                    |
|       19 | prohibitory_weight_over_3.5t          |
|       20 | prohibitory_weight_over_7.5t          |
|       21 | info_bus_station                      |
|       22 | info_crosswalk                        |
|       23 | info_highway                          |
|       24 | info_one_way_traffic                  |
|       25 | info_parking                          |
|       26 | info_taxi_parking                     |
|       27 | mandatory_bike_lane                   |
|       28 | mandatory_left                        |
|       29 | mandatory_left_right                  |
|       30 | mandatory_pass_left                   |
|       31 | mandatory_pass_left_right             |
|       32 | mandatory_pass_right                  |
|       33 | mandatory_right                       |
|       34 | mandatory_roundabout                  |
|       35 | mandatory_straigh_left                |
|       36 | mandatory_straight                    |
|       37 | mandatory_straight_right              |
|       38 | priority_give_way                     |
|       39 | priority_road                         |
|       40 | priority_stop                         |
|       41 | warning_children                      |
|       42 | warning_construction                  |
|       43 | warning_crosswalk                     |
|       44 | warning_cyclists                      |
|       45 | warning_domestic_animals              |
|       46 | warning_other_dangers                 |
|       47 | warning_poor_road_surface             |
|       48 | warning_roundabout                    |
|       49 | warning_slippery_road                 |
|       50 | warning_speed_bumper                  |
|       51 | warning_traffic_light                 |
|       52 | warning_tram                          |
|       53 | warning_two_way_traffic               |
|       54 | warning_wild_animals                  |
|       55 | other_restriction_ends_80             |
|       56 | prohibitory_speed_limit_120           |
|       57 | warning_priority_at_next_intersection |
|       58 | prohibitory_no_vehicles               |
|       59 | warning_bend                          |
|       60 | warning_road_narrows                  |
|       61 | warning_traffic_jam                   |
|       62 | warning_icy_road                      |
|       63 | other_restriction_ends                |
|       64 | other_restriction_ends_overtaking     |
|       65 | priority_road_ends                    |

The inference results are in JSON format, as in the following example:

```json
{
    "iso_timestamp": "2024-11-04T12:50:48.697684",
    "class_ids": [
        22.0, // info_crosswalk
        40.0 // priority_stop
    ],
    "confidences": [
        0.7705173492431641, // confidence info_crosswalk
        0.29842549562454224 // confidence priority_stop
    ]
}
```

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


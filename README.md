# Auto Guard

This repository provides solution that enable the software devleoper and tester for SDV to identify bugs/issues and deploy updated software in the Vehicle.
the following Eclipse SDV projects:
* [Ankaios](https://eclipse-ankaios.github.io/ankaios/latest/) - an embedded container and workload orchestrator targeted at automotive HPCs
* [eCAL](https://ecal.io/) – a fast communication middleware following the pub-sub principle
* [Ankaios Dashboard](https://github.com/FelixMoelders/ankaios-dashboard) – a graphical user interface for the Ankaios orchestrator

The repository additionally uses the MQtt Broker service provided by:
* [HiveMQ](https://www.hivemq.com/) - MQTT Broker service built for flexibility, security, and scalability

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Roadmap](#roadmap)


## Links

- [Ankaios docs](https://eclipse-ankaios.github.io/ankaios/0.5/)
- [Ankaios Dashboard](https://github.com/FelixMoelders/ankaios-dashboard)
- [Ankaios quickstart](https://eclipse-ankaios.github.io/ankaios/0.5/usage/quickstart/)
- [eCAL docs](https://eclipse-ecal.github.io/ecal/)
- [Podman](https://docs.podman.io/en/v4.9.3/)
- [What are devcontainers?](https://containers.dev/)

# Description
This product enables a fleet manager or application developer to build and deploy multi-architecture containerized workloads via a CI/CD pipeline to either one vehicle or the entire fleet.
The workload provided in this repository can detect predefined events and abnormal sensor values and report them to a cloud backend for a developer to evaluate and improve algorithms.
the implemented example workload is set up to detect emergency breaking events and to create reports including attached vehicle data.



![Context View](diagrams/architecture_diagram.PNG)

## Architecture

The repository contains the following Ankaios workloads
- Log Publisher App
- Administrator workload

It also contains the developer tools
- Synthetic Data Generator
- CI/CD pipeline script
and cloud the application
- Reporting API (backend) including a web GUI

### Workload Administrator

The `Workload Administrator` connects to an MQTT broker hosted in the Cloud to recieve the deployment workload specification. It communicates with the Ankaios server over its control interface to perform the following actions on one of the HPCs:
- start containerized workloads
- update containerized workloads
- delete containerized workloads
The `Workload Administrator` is started by Ankaios at the start of the vehicle.

### Log Publisher App
This is an example workload which is available in this repository. The log publisher app subscribes 
to the topic `eCAL measurment` to retrieve dynamic vehicle sensor data to detect an emergency break 
event (trigger). It then communicates with the `Reporting REST API` to submit recorded sensor data 
in case of a trigger event detection.    
The `Log Publisher App` is not started during the vehicle start but is created remotely.

### Synthetic Data Generator
The `Synthetic Data Generator` is reponsible for artificially producing dynamic vehicle sensor data 
to create an emergency breaking scenario. It publishes its sensor data via eCAL to the topic `eCAL measurement`. 
The synthetic data can be used to test and validate the trigger event detection logic in the `Log Publisher App`. 
In the real test vehicle setup this component is replaced by in-vehicle components publishing real 
sensor data to this very topic. 

### Reporting API
The reporting API is our Cloud Application that will be used to both receive the reports 
(they'll be posted at `POST /api/reports`) and to visualize them in a user-friendly UI at `/reports`.


# Installation

## Running the application

### Prerequisites
Docker and VScode with Dev Container extension. Open the Dev Container in VScode as usual. If it does not work for you, try the following steps:

```shell
docker build -t shift2sdv-dev:0.1 --target dev -f .devcontainer/Dockerfile .
```

Once done, you can start the container and run a bash shell in it:
```shell
docker run -it --privileged --name shift2sdv-dev -v <absolute/path/to>/challenge-shift-to-sdv:/workspaces/shift2sdv -p 25551:25551 --workdir /workspaces/shift2sdv shift2sdv-dev:0.1 /bin/bash
````

### Reports dashboard (Outside the Dev Container)
From the project folder, navigate to:
```shell
cd backend/reports-backend
```

Run docker/podman compose to build and start the reports dashboard:
```shell
docker compose build
docker compose down
docker compose up
```

Leave the terminal open. The dashboard will be available at [this link](http://localhost:5010/reports).

### Ankaios cluster
Run the following command to build the container images and start the development deployment:

```shell
scripts/restart_shift2sdv
```

### Building the applications with the CI/CD pipeline
Inside your Dev Container, log into your container registry with docker. In this repository, a dedicated dockerhub registry is used and already filled with the containerized workloads for demonstration purposes. If you want to update the applications, run
```shell
scripts/cicd-build-apps-multi-arch
```
to rebuild and reupload the multi architecture container images to the container registry.

### Deploying the example application via MQTT
Replace `REPORT_DASHBOARD_URI` value inside `scripts/cicd-last-step` using the reports dashboard address.
If you are running the reports dashboard locally, you can specify the host's ip address.

When done, you can deploy the `Log Publisher App` with
```shell
scripts/cicd-last-step
```
This sends out the MQTT message to start the workload on the target device. the script is made to stop the `Log Publisher App` after a minute again.
You can also manually deploy (start or update) an application using MQTT by either sending an Ankaios Manifest to `vehicle/{ID}/manifest/apply` (`ID` can be anything or _all_ for rollout to the entire fleet), or sending a JSON (example defined in [scripts/cicd-last-step](scripts/cicd-last-step)) to `/vehicle/{ID}/workload/start`.
A workload can be stopped by sending the exact same manifest to `vehicle/{ID}/manifest/delete` or just sending the name of the workload (no JSON, just a string) to `/vehicle/{ID}/workload/stop`.

### Use synthetic data

In order to test the `Log Publisher App`, we have created the `synthetic_vdy` app to publish synthetic measurements to the `vehicle_dynamics_synthetic` topic. Run

```shell
cd apps/synthetic_vdy
python3 -u ./synthetic_vdy_app.py
```

Critical reports will appear on the Reporting dashboard when the `Log Publisher App` is running.

## Summary
- `Workload Administrator` application is ran using Ankaios at vehicle startup and listens for workload updates over MQTT
- A newly created containerized application `Log Publisher App` is built, pushed to a container registry and deployed to the vehicle over MQTT (which makes the `Workload Administrator` app and to start it over Ankaios)
- Via MQTT, the vehicle workload state change and regular updates of the vehicle are received
- On the Ankaios Dashboard, the running application is visible
- The `Log Publisher App` subscribes to eCAL data, detects an emergency brake and uploads the recording to the cloud over a REST API
- Emergency brake reports are visible in the GUI
- Via MQTT, the `Log Publisher App`'s trigger condition can be updated, different reports show up on the GUI
- Via MQTT, the `Log Publisher App` can be stopped again
- The MQTT message received  indicate it has in fact stopped
- On the Ankaios Dashboard, the running `Log Publisher App` application has disappeared

# Roadmap
More features have been planned for possible future releases
* **Dynamic Triggers Configuration**: The current release of the "Log Publisher App" only supports recognition 
of "Emergency Break" events. Our plan to support more triggers is to move away from the current hard-coded approach
and to instead provide the triggers configuration trough MQTT. References for this feature can be found at 
[dynamic-triggers.py](assets/dynamic-triggers.py) and [sample-dynamic-triggers](assets/sample-dynamic-triggers.json)
* **Attach Video to Report**: The current release reports are formed mostly by vehicle_dynamics data. 
In order to provide even more detailed information for the manufacturers, we'd like to provide video data 
together with the report

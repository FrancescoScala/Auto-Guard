# Auto Guard

This repository provides solution that enable the software devleoper and tester for SDV to identify bugs/issues and deploy updated software in the Vehicle.
the following Eclipse SDV projects:
* [Ankaios](https://eclipse-ankaios.github.io/ankaios/latest/) - an embedded container and workload orchestrator targeted at automotive HPCs
* [eCAL](https://ecal.io/) – a fast communication middleware following the pub-sub principle
* [Ankaios Dashboard](https://github.com/FelixMoelders/ankaios-dashboard) – a graphical user interface for the Ankaios orchestrator

The repository additionally uses the MQtt Broker service provided by:
* [HiveMQ](https://www.hivemq.com/) - MQTT Broker service built for flexibility, security, and scalability


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
This is an example workload which is available in this repository. The log publisher app subscribes to the topic `eCAL measurment` to revieve dynamic vehicle sensor data to detect an emergency break event (trigger). It then communicates with the `Reporting REST API` to submit recorded sensor data in case of a trigger event detection.
The `Log Publisher App` is not started during the vehicle start but is created remotely.

### Synthetic Data Generator
The `Synthetic Data Geneator` is reponsible for artificially producing dynamic vehicle sensor data to create an emergency breaking scenario. It publishes its sensor data via eCAL to the topic `eCAL measurement`. The synthetic data can be used to test and validate the trigger event detection logic in the `Log Publisher App`. In the real test vehicle setup this component is replaced by in-vehicle components publishing real sensor data to this very topic. 

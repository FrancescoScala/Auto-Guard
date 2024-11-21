# Hackathon Documentation

## Scenario
As a company, I want to deploy a new application (or an updated version) to either a specific vehicle or to my entire fleet at once. This needs to be possible fully remotely: manually and at the end of my CI/CD pipeline. It also has to include the scenario to update a switched-off vehicle immediately when it comes back online.

### Used technologies
*MQTT*: utilizing its secure pub/sub system and retention mechanism
*Ankaios*: starting, stopping and updating containerized workloads on multiple in-vehicle HPCs and ECUs
*eCAL*: reading and recording either live streamed vehicle data or previously recorded vehicle data for development purposes
*containerization*: running agnosticly built applications in sandboxed environments with minimal system dependencies

## Example implementation
We created an application `Workload Administrator` which subscribes to MQTT topics to receive workloads to start, update or delete in the vehicle. It listens to updates for either all vehicles or just its own vehicle. Upon receiving a message, it forwards the respective action to Ankaios and reports back the state changes via MQTT. Also, the state of all the running workloads is reported regularly via MQTT for remote monitoring purposes.
The application is running in the vehicle at startup as part of the initial Ankaios state file.

As a newly created application `Log Publisher App` that shall be deployed to the fleet, we created an containerized workload (written in Python) which reads and records streamed eCAL data (either live or previously recorded and played back). It detect a certain trigger event based on a trigger condition. The formula for the trigger condition (based on eCAL data) is customizable remotely via MQTT. For our example application, we chose the detection of an emergency brake. The recorded data around the detected trigger event (a few seconds before and after the event) is uploaded to a cloud server via a REST API and saved in a database. The list of occurred events can be seen on a web application running in the cloud as well.
The entire workload is built, pushed to a container registry in the cloudand remotely deployed via MQTT via the in-vehicle `Workload Administrator`.

## Installation

### Prerequisites
Docker and VScode with Dev Container extension. Open the Dev Container in VScode as usual. If it does not work for you, try the following steps:

```shell
docker build -t shift2sdv-dev:0.1 --target dev -f .devcontainer/Dockerfile .
```

Once done, you can start the container and run a bash shell in it:

```shell
docker run -it --privileged --name shift2sdv-dev -v <absolute/path/to>/challenge-shift-to-sdv:/workspaces/shift2sdv -p 25551:25551 --workdir /workspaces/shift2sdv shift2sdv-dev:0.1 /bin/bash
```

### Building the applications with the CI/CD pipeline
Inside your Dev Container, log into your container registry with docker. In this repository, a dedicated dockerhub registry is used and already filled with the containerized workloads for demonstration purposes. If you want to update the applications, run
```shell
scripts/cicd-build-apps-multi-arch
```
to rebuild and reupload the multi architecture container images to the container registry.

### Deploying the example application via MQTT
When done, you can deploy the `Log Publisher App` with
```shell
scripts/cicd-last-step
```
This sends out the MQTT message to start the workload on the target device. the script is made to stop the `Log Publisher App` after a minute again.

You can also manually deploy (start or update) an application using MQTT by either sending an Ankaios Manifest to `vehicle/{ID}/manifest/apply` (`ID` can be anything or _all_ for rollout to the entire fleet), or sending a JSON (example defined in [scripts/cicd-last-step](scripts/cicd-last-step)) to `/vehicle/{ID}/workload/start`.

A workload can be stopped by sending the exact same manifest to `vehicle/{ID}/manifest/delete` or just sending the name of the workload (no JSON, just a string) to `/vehicle/{ID}/workload/stop`.


### Reporting API and dashboard
In the project folder, run the following command to build and start the Reporting API and Dashboard:
```shell
cd backend/reports-backend
docker compose down --remove-orphans || true
docker compose up --build -d
```
The dashboard will be available at [this link](http://localhost:5010/reports).

### Ankaios cluster
Run the following command to build the container images and start the development deployment:

```shell
scripts/restart_shift2sdv
```

## Use synthetic data

In order to test the `Log Publisher App`, we have created the `synthetic_vdy` app to publish synthetic measurements to the `vehicle_dynamics_synthetic` topic. Run

```shell
cd apps/synthetic_vdy
python3 -u ./synthetic_vdy_app.py
```

Critical reports will appear on the Reporting dashboard when the `Log Publisher App` is running.

## Summary
- `Workload Administrator` application is ran using Ankaios at vehicle startup and listens for workload updates over MQTT
- a newly created containerized application `Log Publisher App` is built, pushed to a container registry and deployed to the vehicle over MQTT (which makes the `Workload Administrator` app and to start it over Ankaios)
- via MQTT, the vehicle workload state change and regular updates of the vehicle are received
- on the Ankaios Dashboard, the running application is visible
- the `Log Publisher App` subscribes to eCAL data, detects an emergency brake and uploads the recording to the cloud over a REST API
- emergency brake reports are visible in the GUI
- via MQTT, the `Log Publisher App`'s trigger condition can be updated, different reports show up on the GUI
- via MQTT, the `Log Publisher App` can be stopped again
- the MQTT message received  indicate it has in fact stopped
- on the Ankaios Dashboard, the running `Log Publisher App` application has disappeared

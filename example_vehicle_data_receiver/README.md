# Example Vehicle Data Receiver

The vehicle data receiver receives the following real time data:

- GNSS position
- front radar long range sensor detected objects with distances
- front left and front right mid range radar sensor detected objects with distances
- front camera traffic sign detection inference results (bounding boxes with class id and probability)

## Run

TODO!: Currently, there is a `demo_publisher.py` containing a example data publisher just to test the subscriber workload executed in `main.py`. The demo sender must be removed later!

Inside the devcontainer run the following:

Start the demo_publisher.

```shell
python3 example_vehicle_data_receiver/demo_publisher.py
```

Open a new shell inside the devcontainer and start the subscriber which outputs vehicle data on the terminal:

```shell
python3 example_vehicle_data_receiver/main.py
```
# Example Application

The example application show how data from the vehicle can be received by an application running in the vehicle.

## Build

When running `restart-shift2sdv`, or explicitly the `build-apps` script, the Example App will be build and containerized automatically as `ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/example_app:latest`.

Of course, you are free to build manually if needed by calling the following command from the example_app folder:

```shell
podman build -t example_app:latest .
```

**Note:** Inside the test-vehicle the Example App will run on ARM-Platform. Test the build by running the command above and ask the hack coaches to build your image for ARM to run it inside the test vehicle.

TODO
# Symphony Provider

The Symphony provider connects the Symphony meta-orchestrator running in the the cloud with the Ankaios embedded orchestrator running in the vehicle.

## Build

When running `restart-shift2sdv`, or explicitly the `build-apps` script, the Symphony Provider will be build and containerized automatically as `ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/symphony_provider:latest`.

Of course, you are free to build manually if needed by calling the following command from the symphony_provider folder:

```shell
podman build -t symphony_provider:latest .
```

**Note:** Inside the test-vehicle the Symphony Provider will run on ARM-Platform. Test the build by running the command above and ask the hack coaches to build your image for ARM to run it inside the test vehicle.

TODO
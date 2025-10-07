# AeroRoute-System
A Django-based flight route management system that allows users to add airport routes, search specific nodes, and analyze the longest and shortest routes based on duration.

## Debugging with Docker & VS Code

To debug the app inside Docker with VS Code using debugpy:

1. By default the docker-compose configuration starts the container with `DEBUGPY=1` and `DEBUGPY_WAIT=1`.
	- This makes the container start Django under `debugpy` and wait for a debugger to attach on port 5678.

2. Start the container (build on first run):

```powershell
docker-compose up --build
```

3. In VS Code select the `Attach to Django in Docker` debug configuration and start debugging (F5).

4. To avoid waiting for a debugger, set `DEBUGPY_WAIT=0` in `docker-compose.yml` or override the env var when starting the container.

5. If VS Code cannot attach, ensure the Python interpreter in VS Code matches the environment used to install dependencies inside the container and that port 5678 is not blocked by a firewall.

## Pre-requisites

- Podman 
- The fish shell to run the scripts
 
## Set up

Create a .env file from the template `.env.template`. 

```shell
cp -i .env.template .env
```
Edit the `.env` file and add the keys. You'll need Gemini, OpenAI and Tavily API keys.

For Kestra Open Source, the `SECRET_*` entries must be base64-encoded versions of the raw provider keys. Two details matter:

1. encode the key **without** a trailing newline
2. keep the encoded value on **one line** in `.env`

This works well on Linux:

```shell
echo -n 'your-key' | base64 -w0
```

For example:

```shell
echo -n "$GEMINI_API_KEY" | base64 -w0
echo -n "$TAVILY_API_KEY" | base64 -w0
echo -n "$OPENAI_API_KEY" | base64 -w0
```

Once the `.env` file is in place, start the containers:

```shell
make up
```

`make up` starts the rootless Podman API socket before launching Kestra, so Docker-based Kestra plugins can talk to Podman through `/var/run/docker.sock`.

Once kestra is up and runnig, you can upload the flows:

```shell
make load_flows
```

The flows in the `flows/` folder have been downloaded from https://github.com/DataTalksClub/llm-zoomcamp/tree/main/03-orchestration/flows

Point your local browser to http://localhost:28080


## FAQ

### Why do Docker-based Kestra tasks fail under Podman with `Connection refused`?

Those tasks use Kestra's Docker client internally. Under Podman, they only work if the Podman API socket is running and mounted into the Kestra container at `/var/run/docker.sock`.

This project's `make up` target now starts `podman.socket` automatically and verifies that the socket path is a real Unix socket before calling `podman compose up -d`.

If you still see the error, check:

```shell
systemctl --user status podman.socket
ls -ld "$(podman info --format '{{.Host.RemoteSocket.Path}}')"
```

If that path is a directory instead of a socket, remove it and rerun `make up`.

### Why are you using port `28080`?

Because I usually have other stuff running in port `8080`.

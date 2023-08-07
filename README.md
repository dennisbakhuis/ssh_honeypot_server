# SSH Honeypot Server
A simple Honeypot Server written in Python. The design is mostly based on [Arturovergara's design](https://github.com/arturovergara/ssh-honeypot) which I have restructured and added some addtional features.

The server will start an SSH server which always returns a failed login attempt. The server will log the IP address, username and password used for the login attempt. The server will also log IP details from [ipinfo.io](https://ipinfo.io/). For this a token is required.

## Requirements / Installation / Usage (locally)
The only package required is [paramiko](https://www.paramiko.org/). This can be installed using pip:
```bash
pip install paramiko
```

I generally work with Poetry and therefore, there is also a pyproject.toml file included. This can be used to install the dependencies using Poetry:
```bash
poetry install
```

To start the server locally, simply run the following command:
```bash
python ssh_honeypot/main.py
```

### Configuration
The server can be configured with command line parameters or environment variables with the latter taking precedence. The following parameters are available:
* -p, --port: The port on which the server should listen. Default: 2222
* -c, --max-connections: The maximum number of connections the server should accept. Default: 10
* -t, --ip-info-api-token: The token for ipinfo.io. Default: None
* -f, --file: The file to which the logs should be written. Default: ./honeypot.jsonl

The following environment variables are available and override the command line parameters and defaults:
* HONEYPOT_PORT: The port on which the server should listen.
* HONEYPOT_MAX_CONNECTIONS: The maximum number of connections the server should accept.
* HONEYPOT_IP_INFO_API_TOKEN: The token for ipinfo.io.
* HONEYPOT_OUTPUT_FILE: The file to which the logs should be written.

## Building Docker Container

```bash
poetry export --without-hashes --format=requirements.txt > requirements.txt
docker build -t ssh-honeypot --platform linux/amd64 .
```

### Runing the locally build container

```bash
docker run \
  -v ./local/:/data/ \
  -p 2222:2222 \
  -it \
  --rm \
  --platform=linux/amd64 \
  ssh-honeypot:latest
```

### Pushing the container to Docker Hub
To push it to your own Docker Hub, you need to tag it and push it to your own Docker Hub repository. Change the <dennisbakhuis> to your own Docker Hub username.

```bash
docker tag ssh-honeypot:latest dennisbakhuis/ssh-honeypot:latest
docker push dennisbakhuis/ssh-honeypot:latest
```

## Usage with Docker-compose
The server can also be run using docker-compose. The following docker-compose.yml file can be used to run the server:

```yaml
ssh-honeypot:
  image: dennisbakhuis/ssh-honeypot:latest
  container_name: ssh-honeypot
  networks:
    - t2_proxy
  environment:
    - PUID=$PUID
    - PGID=$PGID
    - TZ=Europe/Amsterdam
    - HONEYPOT_IP_INFO_API_TOKEN=$HONEYPOT_IP_INFO_API_TOKEN
  volumes:
    - /etc/localtime:/etc/localtime:ro
    - $DOCKERDIR/ssh_honeypot/:/data/
  ports:
    - 2222:2222
  restart: unless-stopped
```

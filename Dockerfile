## Build: docker build --force-rm --no-cache -t "qasa" .
## Run Interactive: docker run -it qasa
## Run Interactive: docker run -it qasa /bin/bash
## Run Daemon: docker run -d qasa
## apt-get install --reinstall ca-certificates

## Debian-base build...
FROM python:3.10.6-slim-buster
ADD . /app
RUN pip install -r /app/requirements.txt
CMD ["python3", "/app/qasa.py", "exec", "scheduler"]

##
### Alpine Linux build...
# FROM python:3.10.6-alpine3.16
# RUN set -ex && apk add --no-cache gcc libc-dev
# ADD . /app
# RUN pip install -r /app/requirements.txt
# CMD ["python3", "/app/qasa.py", "exec", "scheduler"]
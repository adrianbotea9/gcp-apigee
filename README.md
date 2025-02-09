# gcp-apigee

## Features
    - List all apps in the Apigee Org
    - List apps belonging to a sprecific developer
    - Create new app with specific parameters
    - Docker config for easy deployment

## Command line arguments
 Argument | Required | Description 
 --- |:---:| ---  
 --organization | yes | Org id
 --credentials | yes | Path to SA json
 --action | yes | Action to perform
 --dev-mail | for list-developer, create | Developer mail address 
 --app-name | for create | App name to be created
 --callback-url | no | Callback url for new app
 --description | no | Description for new app


## Using Docker

- Build docker image:
```bash
docker build -t apigee-gcp .
```

- Use docker image:

## Environment variables

- `GOOGLE_APPLICATION_CREDENTIALS`: PAth to GCP credentials json file inside the container

## Volume mounts

- mount credentials file to make it accesible by the container: `/path/to/credentials.json:/credentials.json`

## Actions

- list all apps: [--action list-all]
- list developer apps: [--action list-developer]
- create new app: [--action create]

1. List all apps:
```bash
docker run -v /path/to/credentials.json:/credentials.json \
    -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
    apigee-manager \
    --organization ORG_ID \
    --credentials /credentials.json \
    --action list-all
```

2. List developer apps:
```bash
docker run -v /path/to/credentials.json:/credentials.json \
    -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
    apigee-manager \
    --organization ORG_ID \
    --credentials /credentials.json \
    --action list-developer \
    --dev-mail dev@gmail.com
```

3. Create new app: <br />
Optional args:
[--callback-url Callback url for new app]
[--description description for new app]
```bash
docker run -v /path/to/credentials.json:/credentials.json \
    -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
    apigee-manager \
    --organization ORG_ID \
    --credentials /credentials.json \
    --action create \
    --dev-mail dev@gmail.com \
    --app-name exampleApp1 \
```

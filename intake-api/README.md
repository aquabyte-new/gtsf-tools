# Intake API
The intake API is our interface between the UI and our database. It is a simple FastAPI application that talks to a postgres database with the tables `gtsf_collections` and `gtsf_fish`. In production we use the FishFact database. 

## Development
The API is set up to have two modes, production and local. This is configured via the ENV variable which defaults to local if none is set. Run the local API server via `just serve`. The local version is set up to use a local postgres database specific to @sam but this can be easily extended when the need arises.

## Deployment
Most changes can be released with a simple `just release` command. Certain changes may require you to update
the systemd definition if you need to add an environmental variable or update the startup command.

### Modifying the systemd service
The unit file for the service is defined in this file: `/etc/systemd/system/gtsf-api.service`. In it we set:
 - host: 0.0.0.0
 - port: 8821
 - run with automatic reloading (so deploys are easier)
 - environmental variables like `ENV`, `AWS_DEFAULT_REGION`, and others
 
To modify run:
 1) `sudo nano /etc/systemd/system/gtsf-api.service`
 2) `sudo systemd daemon-reload`
 3) `sudo systemd restart gtsf-api`

### Looking at logs
You can view service logs via `sudo systemctl status gtsf-api`.
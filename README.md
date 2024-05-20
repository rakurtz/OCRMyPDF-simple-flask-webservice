# Webservice with a drag an drop field to upload PDFs for OCR
## how to run
```
# create the external network
docker network create ocr-external-network

# run with docker compose
cd /path/to/compose.yaml
docker compose up -d
```

After that the service should be available at http://host:3000


## done
- isolate ocrmydf docker to not be able to communicate with the outside world
- add cron_restart_script.sh (instructions inside file)
- handle errors (for example encrypted pdfs)
- added better results
- add visual feedback for the time of processing (very basic)

## Todo:
- migrate to production ready server (still flask developtment server)
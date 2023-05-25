# Cloudrun Deployment Example
Deploying Django apps to Google Cloud Run using AlloyDB (via auth proxy sidecar) and GitHub Actions.

*Work in progress - figuring out the workflow first with a hello-world app with postgres-like db, then will apply to a more applicable example*

Resources:
* https://github.com/google-github-actions/deploy-cloudrun
* https://phac-garden.vercel.app/other/cloudsql
* https://cloud.google.com/alloydb
* https://cloud.google.com/run/docs/deploying#sidecars

Steps 
* Build app
* Add tests
* Containerize
* Add to Artifact Registry (turn on vunerability scanning) and add tag eg :latest or my-image@sha...)
* Activate cloud run
* Add sidecar yaml

Next steps 
* add secrets
* modify to connect to db (or fork an existing project and use in this example)




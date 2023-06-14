### Initial GCP set up 

Authorize GCP:
* gcloud auth login
Set to project:
* gcloud config set project <your project name>
Check to make sure correct:
* gcloud config get-value project 
Edit initial-gcp-sa-api-setup.sh file with variables pointing to right project/ repo
Make script executable:
* chmod +x ./djangoproject/deploy/initial-gcp-sa-api-setup.sh

Run initial set up:
* ./djangoproject/deploy/initial-gcp-sa-api-setup.sh

Add cloudbuild.yaml file here with steps to deploy

<!-- For open telemetry: -->


#!/bin/bash
# Enables Cloud Run, Cloud Build and Artifact Registry APIS
# Creates or binds associated Service Accounts with permissions

set -ex
# ----- ENVIRONMENT VARIABLES -----
# Replace project id and artifact_registry_name variables with your projects 
PROJECT_ID="phx-01h1yptgmche7jcy01wzzpw2rf" \
REGION="northamerica-northeast1" \
ARTIFACT_REGISTRY_REPO_NAME="hello-world-app" \
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")

GITHUB_REPO_NAME="cloudrun-deployment-example"
GITHUB_REPO_OWNER="PHACDataHub"
CLOUD_BUILD_TRIGGER_NAME="hello-world-deploy-trigger"
CLOUD_BUILD_CONFIG_PATH="djangoproject/deploy/cloudbuild.yaml"

SQL_INSTANCE="hello-world-sql-instance"
DB_NAME="hello-world-db"

# Set google cloud storage bucket for static files storage
GCS_BUCKET_NAME="hello_world_bucket"


# ----- ARTIFACT REGISTRY -----
# Enable Artifact Registry to store container images for Cloud Run to use 
gcloud services enable artifactregistry.googleapis.com

# Create Artifact Repo within the Artifact Registry
gcloud artifacts repositories create ${ARTIFACT_REGISTRY_REPO_NAME} \
   --repository-format=docker \
   --location=${REGION} \
   --description=${ARTIFACT_REGISTRY_REPO_NAME}

# Authorize docker to push images to artifact registry
gcloud auth configure-docker ${REGION}-docker.pkg.dev


# ----- CLOUD BUILD -----
# Set up Cloud Build  (https://cloud.google.com/sdk/gcloud/reference/beta/builds/triggers/create/github)
# Enable Cloud Build service and source repo
gcloud services enable cloudbuild.googleapis.com sourcerepo.googleapis.com

# ** Need to add cloudbuild.yaml to repo and the in Google Cloud console, connect Cloud Build to GitHub Repository 

# Add cloud build trigger (this is set to be triggered on push to main branch)

gcloud builds triggers create github \
  --name=${CLOUD_BUILD_TRIGGER_NAME} \
  --region ${REGION} \
  --repo-name=${GITHUB_REPO_NAME} \
  --repo-owner=${GITHUB_REPO_OWNER} \
  --branch-pattern="^main$" \
  --build-config=${CLOUD_BUILD_CONFIG_PATH} \
  --include-logs-with-status \
  --no-require-approval


# ----- CLOUD RUN -----
# Enable Cloud Run Service    
gcloud services enable run.googleapis.com

# gcloud projects add-iam-policy-binding $PROJECT_ID --member=MEMBER --role=roles/run.admin


# Bind permissions for cloud build to push to cloud run 
# gcloud projects add-iam-policy-binding $PROJECT_ID \
# --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
# --role=roles/run.admin \
# --role=roles/iam.serviceAccountUser
# --role=roles/artifactregistry.writer

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:service-249044526600@gcp-sa-cloudbuild.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.serviceAgent" \
    --role=roles/run.admin \
    --role=roles/artifactregistry.writer \
    --role=roles/iam.serviceAccountUser


# ---- CLOUD SQL (postgres) -----
# Create SQL instance
gcloud sql instances create $SQL_INSTANCE \
    --project $PROJECT_ID \
    --database-version POSTGRES_13 \
    --tier db-f1-micro \
    --region $REGION

# Create Database
gcloud sql databases create $DB_NAME \
    --instance $SQL_INSTANCE

# Set DB username and password **MOVE TO SECRETS!
gcloud sql users create postgres_user \
    --instance $SQL_INSTANCE \
    --password postgres_password

# ----- CLOUD STORAGE BUCKET -----
# Enable API
gcloud services enable \
    storage-component.googleapis.com \
    storage-api.googleapis.com 

# * Make bucket (needed to store .env?)
gsutil mb -p $PROJECT_ID -l $REGION -b on gs://$GCS_BUCKET_NAME

# Bind permissions for cloud run to talk to bucket 
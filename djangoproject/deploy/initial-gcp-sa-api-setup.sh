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

SQL_INSTANCE="hello-world-instance"
DB_NAME="hello-world-db"
DB_SECRET="hello-world-db-password"

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
    --role=roles/iam.serviceAccountUser \
    --role=roles/secretmanager.secretAccessor


# grant compute account access to secrets:
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:249044526600-compute@developer.gserviceaccount.com" \
    --role=roles/secretmanager.secretAccessor \
    --role=roles/cloudsql.client

   



# ---- CLOUD SQL (postgres) -----
# enable APIS
gcloud services enable sqladmin.googleapis.com
gcloud services enable sql-component.googleapis.com

# Create database password:
export DB_PASSWORD=$(openssl rand -base64 16 | tr -dc A-Za-z0-9 | head -c16 ; echo '')
echo -n "${DB_PASSWORD}" | gcloud secrets create hello-world-db-password --replication-policy="user-managed" --locations="${REGION}" --data-file=-

# Create SQL instance



gcloud sql instances create $SQL_INSTANCE \
    --project $PROJECT_ID \
    --database-version=POSTGRES_14 \
    --tier=db-g1-small \
    --region $REGION \
    --root-password="${DB_PASSWORD}

# Create Database
gcloud sql databases create $DB_NAME \
    --instance $SQL_INSTANCE

# Set DB username and password
gcloud sql users create hello-world-user \
    --instance $SQL_INSTANCE \
    --password="${DB_PASSWORD}"

# Create instance connection 
INSTANCE_CONNECTION_NAME=$(gcloud sql instances describe $SQL_INSTANCE --format='value(connectionName)')
echo -n "postgresql://hello-world-user:${DB_PASSWORD}@localhost/${DB_NAME}?host=/cloudsql/${INSTANCE_CONNECTION_NAME}" | gcloud secrets create hello-world-db-connection-string --replication-policy="user-managed" --locations="${REGION}" --data-file=-

# Don't forget to update (potentially)
# 1- file:.env.prod-XXX
# 2- secret: hello-world-env-secret-DATABASE_URL
# create secret, if not exists:
gcloud secrets create "hello-world-env-secret-DATABASE_URL" --replication-policy="user-managed" --locations="${REGION}"
# Then update the secret with:
echo -n "postgresql://hello-world-user:${DB_PASSWORD}@localhost/${DB_NAME}?host=/cloudsql/${INSTANCE_CONNECTION_NAME}" | gcloud secrets versions add "hello-world-env-secret-DATABASE_URL" --data-file=-
# Or copy it from hello-world-db-connection-string
gcloud secrets versions access latest --secret=hello-world-db-connection-string | gcloud secrets versions add "hello-world-env-secret-DATABASE_URL" --data-file=-

# ----- CLOUD STORAGE BUCKET (for static files note - John found this for Django)-----
# Enable API
gcloud services enable \
    storage-component.googleapis.com \
    storage-api.googleapis.com 

# * Make bucket (needed to store .env?)
gsutil mb -p $PROJECT_ID -l $REGION -b on gs://$GCS_BUCKET_NAME

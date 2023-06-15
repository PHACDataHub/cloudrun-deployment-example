
#!/bin/bash

set -ex

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


# Automatic - globally replicated is not allowed in our accounts
# gcloud secrets create epi-t3-env-secret --replication-policy="automatic"
gcloud secrets create hello-world-env-secret --replication-policy="user-managed" --locations="${REGION}"

gcloud secrets versions add hello-world-env-secret --data-file=".env.prod-gcp-danl"
gcloud secrets create "hello-world-env-secret-$v" --replication-policy="user-managed" --locations="${REGION}"
# # add/replace the secret
echo -n "${SECRET}" | gcloud secrets versions add "hello-world-env-secret-$v" --data-file=-



# Allow the service account to read the secrets
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor

# # list and show the secret
# gcloud secrets list
# gcloud secrets versions access latest --secret=hello-world-env-secret
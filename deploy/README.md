# Deployment instructions 
Slowly moving these to shell script (initial-gcp-sa-api-setup.sh) and will add more details there! To run:
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
## But, for now... Deployment options
a) GitHub Actions to run tests on a new Pull Request.  On a push to the main branch, a Cloud Build trigger will run through the steps outlined in [cloudbuild.yaml](./cloudbuild.yaml) to build the docker image, push to the image Artifact Registry and then deploy to Cloud Run (Cloud Run can only be deployed to from the Artifact Registry).

b) Capture the whole CI/CD process with GitHub Actions using [keyless authentication](https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions). Dan brought up a great question - right now it's building the image with GCP, why not pull the build and push steps out of google cloud and only do the deploy to Cloud Run step with GCP.


## Steps to Deploy 
Both options follow the same 
<!-- Google Cloud Run Service Agent service-294163875507@serverless-robot-prod.iam.gserviceaccount.com  -->
### 1. Build app
* Using a simple django app here as an example
* Add tests - a key component to reduce breaking changes with continuous deployment

* Set up DNS and add to approved hosts (in settings.py) if using Django 
*(This is a later step, but penciling in as to not forget)*

### 2. Containerize 
* Add [Dockerfile](../djangoproject/Dockerfile) and [requirements.txt](../djangoproject/requirements.txt) (if not using pdm) to django project folder, and if you would like to run/test locally, create [docker-compose.yaml](../docker-compose.yaml) to root.

*TODO Add database image to this file*
<!-- **Look at using GCP cloud shell or GitHub codespaces if unable to use docker on your machine because of admin privledges**  -->

* To run locally:

    ```$ docker-compose up -d ```

    ```$ docker-compose down ``` to tear down at end

### 3. Install command line tools
For the following steps you'll need the [gcloud](https://cloud.google.com/sdk/docs/install) (Google Cloud resources) 
and [gsutil](https://cloud.google.com/storage/docs/gsutil_install) (Google Cloud Storage) CLIs. 

### 4. Authenticate GCP
Set environment variables (change to your project's values - note REGION should be set to montreal (northamerica-northeast-1) as it's more established)

``` 
export PROJECT_ID="phx-01h1yptgmche7jcy01wzzpw2rf" \
export REGION="northamerica-northeast1" \
export ARTIFACT_REGISTRY_REPO_NAME="hello-world-app" \
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
```

Login to gcloud and set project

```
$ gcloud auth login
$ gcloud config set project $PROJECT_ID
```

### 5. Either set up [Cloud Build trigger](./deployment-instructions/clould-build-trigger-README.md) or [GitHub Actions](./deployment-instructions/github-actions-README.md) 
*Go to associated README file*
### 6. Update Allowed Hosts 
* Get url from Cloud Run UI and then add to allowed hosts in [settings.py](../djangoproject/djangoproject/settings.py)
* *TODO - Dan set up DNS - can we preset this?*
Get url here:
```
CLOUDRUN_SERVICE_URL=$(gcloud run services describe django-cloudrun \
  --platform managed \
  --region $REGION  \
  --format "value(status.url)")
echo $CLOUDRUN_SERVICE_URL
```

### 5. Set up Database (not yet working)
Starting with Postgres per https://cloud.google.com/python/django/run
* Enable service 
``` 
$ gcloud services enable sqladmin.googleapis.com 
```
* download auth proxy & make executatable (see link above)
* Create PostgreSQL instance:

```
gcloud sql instances create hello-world-sql-instance \
    --project $PROJECT_ID \
    --database-version POSTGRES_13 \
    --tier db-f1-micro \
    --region $REGION
```
* Create database 
```
gcloud sql databases create hello-world-db \
    --instance hello-world-sql-instance
```
* Set DB username and password
```
gcloud sql users create postgres_user \
    --instance hello-world-sql-instance \
    --password postgres_password
```

### 6. Cloud Storage bucket
Enable services
```
gcloud services enable \
    storage-component.googleapis.com \
    storage-api.googleapis.com \
```

* Make bucket (needed to store .env?)
gsutil mb -l $REGION gs://$PROJECT_ID/django_bucket

### 7. Secret Manager
```
gcloud config set run/region $REGION
```

add username and password to bucket as .env
```
echo DATABASE_URL=postgres://postgres_username:postgres_password@//cloudsql/$PROJECT_ID:$REGION:hello-world-sql-instance/hello-world-db > .env
echo GS_BUCKET_NAME=$PROJECT_ID/django_bucket >> .env
echo SECRET_KEY=$(cat /dev/urandom | LC_ALL=C tr -dc '[:alpha:]'| fold -w 50 | head -n1) >> .env
```

```
gcloud secrets create application_settings  --replication-policy="user-managed" --locations $REGION --data-file .env
```

Note need this installed:
https://cloud.google.com/sql/docs/postgres/connect-instance-auth-proxy#debianubuntu

following along with this:
https://codelabs.developers.google.com/codelabs/cloud-run-django#6

gcloud builds submit --pack image=gcr.io/${PROJECT_ID}/myimage
<!-- admin_password="$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 30 | head -n 1)"

echo -n "${admin_password}" | gcloud secrets create admin_password --replication-policy="user-managed" --locations $REGION --data-file=-

gcloud secrets add-iam-policy-binding admin_password \
  --member serviceAccount:${CLOUDBUILD} --role roles/secretmanager.secretAccessor -->
### 8. AlloyDB
* Activate (for this we need AlloyDB, Compute Engine, Resource Manager and Service Networking APIs)

```
gcloud services enable \
    alloydb.googleapis.com \
    compute.googleapis.com \
    cloudresourcemanager.googleapis.com \
    servicenetworking.googleapis.com
```
* Add sidecar yaml
* set up private network for AlloyDB

Add AlloyDB client role to service account:
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/alloydb.client"
```
<!-- 
  ------------------------
export NETWORK_NAME='test-network'
export REGION="northamerica-northeast1"
export SUBNETWORK_NAME='test-subnetwork'
export SUBNETWORK_IP_RANGE=10.1.0.0/20
export FIREWALL_NAME='test-firewall'

export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
export PROJECT_NAME=$(gcloud projects describe $PROJECT_ID --format='value(name)')

create network
gcloud compute networks create ${NETWORK_NAME} \
  --project ${PROJECT_ID} \
  --subnet-mode custom

create subnetwork
gcloud compute networks subnets create ${SUBNETWORK_NAME} \
  --project ${PROJECT_ID} \
  --region ${REGION} \
  --network ${NETWORK_NAME} \
  --range ${SUBNETWORK_IP_RANGE}

Need to set firewall rules for network 
$ gcloud compute firewall-rules create $FIREWALL_NAME --network test-network --allow tcp,udp,icmp --source-ranges $SUBNETWORK_IP_RANGE


Allocate an IP address range on new network
gcloud compute addresses create google-managed-services-default \
    --global \
    --purpose=VPC_PEERING \
    --prefix-length=20 \
    --network=${NETWORK_NAME}

private connection
gcloud services vpc-peerings connect \
    --service=servicenetworking.googleapis.com \
    --ranges=google-managed-services-default \
    --network=${NETWORK_NAME} \
    --project=$PROJECT_ID -->

    ----------------------------------------
### Migrations

https://cloud.google.com/blog/topics/developers-practitioners/running-database-migrations-cloud-run-jobs
#### 1. Create a migration Cloud Run job 
(from above)
```
export PROJECT_ID=$(gcloud config get-value project) 
export SERVICE_NAME=hello-world
export REGION=northamerica-northeast1

# Get the image name (this includes SHA)
export IMAGE_NAME=$(gcloud run services describe $SERVICE_NAME --region $REGION --format "value(spec.template.spec.containers[0].image)")

export IMAGE_NAME=northamerica-northeast1-docker.pkg.dev/$PROJECT_ID/hello-world-app/hello-world


# Get the Cloud SQL Instance
export SQL_INSTANCE=$(gcloud run services describe $SERVICE_NAME --region $REGION --format  "value(spec.template.metadata.annotations.'run.googleapis.com/cloudsql-instances')")
# example: phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:myinstance

# Create Job
gcloud beta run jobs create migrate-test \
  --image $IMAGE_NAME \
  --region $REGION \
  --command "python manage.py makemigrations" && python manage.py migrate"
    <!-- --set-cloudsql-instances $SQL_INSTANCE \ -->

```
#### 2. Add migration step to cloudbuild.yaml
```
  - id: "server migrate"
    name: "gcr.io/google.com/cloudsdktool/cloud-sdk:slim"
    entrypoint: gcloud
    args: ["beta", "run", "jobs", "execute",  "migrate-database",
           "--region", $_REGION, "--wait"]
```

## When working with SQL lite, add migration to deployment by

#### 1. Add the following to settings.py
https://docs.djangoproject.com/en/4.2/ref/csrf/
```
CSRF_TRUSTED_ORIGINS = [
    'https://hello-world-from-cloud-build-trigger-vlfae7w5dq-nn.a.run.app',
]
```
(replace with your Cloud Run service URL)

#### 1. Add [entrypoint.sh](../djangoproject/entrypoint.sh) to your djangoproject (along side the Dockerfile)

#### 3. Modify Dockerfile to specify entrypoint script and change the permissions of file. 


## Open Telemetry 

Deploy as sidecar:

* https://cloud.google.com/blog/products/serverless/cloud-run-now-supports-multi-container-deployments
* https://github.com/GoogleCloudPlatform/opentelemetry-cloud-run

Enable Cloud Trace and Monitoring
```
gcloud services enable cloudtrace.googleapis.com
gcloud services enable monitoring.googleapis.com
```

Add these roles to Cloud Run service account:
* roles/monitoring.metricWriter
* roles/cloudtrace.agent
* roles/logging.logWriter

Cloud build needs these ones:
* roles/iam.serviceAccountUser
* roles/storage.objectViewer
* roles/logging.logWriter
* roles/artifactregistry.createOnPushWriter
* roles/run.admin


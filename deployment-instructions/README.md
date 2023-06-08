## Deployment options
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

### 5. Either set up [Cloud Build trigger](clould-build-trigger-README.md) or [GitHub Actions](github-actions-README.md) 
*Go to associated README file*
### 6. Update Allowed Hosts 
* Get url from Cloud Run UI and then add to allowed hosts in [settings.py](../djangoproject/djangoproject/settings.py)
* *TODO - Dan set up DNS - can we preset this?*

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
add username and password to bucket as .env
```
echo DATABASE_URL=postgres://postgres_username:postgres_password@//cloudsql/$PROJECT_ID:$REGION:hello-world-sql-instance/hello-world-db > .env
echo GS_BUCKET_NAME=$PROJECT_ID/django_bucket >> .env
echo SECRET_KEY=$(cat /dev/urandom | LC_ALL=C tr -dc '[:alpha:]'| fold -w 50 | head -n1) >> .env
```
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
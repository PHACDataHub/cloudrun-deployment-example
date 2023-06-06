## Deployment options
1. GitHub Actions to run tests on pull request, then on push to main, a cloud build trigger will run steps to build the docker image, push to image artifact registry and deploy to cloud run (current way discribed below)

2. Capture the whole CI/CD process with GitHub Actions (now working on)


## Steps to Deploy 
<!-- Google Cloud Run Service Agent service-294163875507@serverless-robot-prod.iam.gserviceaccount.com  -->
### 1. Build app
* Using a django app here as an example
* Add tests - a key component to reducing breaking changes with continuous deployment
<!-- * Add githubs workflow file  -->

* Set up DNS and add to approved hosts (in settings.py) if using Django

### 2. Containerize 
* Add Dockerfile and requirements.txt to django project folder, if would like to run locally, create docker-compose.yaml to root.

*TODO Add database image to this file*
<!-- **Look at using GCP cloud shell or GitHub codespaces if unable to use docker on your machine because of admin privledges**  -->

To run locally:

```$ docker-compose up -d ```

```$ docker-compose down ``` to tear down at end

### 3. Authenticate GCP
For the following steps you'll need the [gcloud](https://cloud.google.com/sdk/docs/install) and [gsutil](https://cloud.google.com/storage/docs/gsutil_install) clis. 

Set environment variables (change to your project's values)

``` 
export PROJECT_ID="phx-01h1yptgmche7jcy01wzzpw2rf" \
export REGION="northamerica-northeast1" \
export ARTIFACT_REGISTRY_REPO_NAME="hello-world-app" \
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
```

Login to gcloud and set project

```$ gcloud auth login```

```$ gcloud config set project $PROJECT_ID```

### 4. Either set up [Cloud Build trigger](clould-build-trigger-README.md) or [github actions](github-actions-README.md) 

* Add url from cloud run to approved hosts in settings.py after first deployment

### 5.Set up Database (not yet working)
Starting with Postgres per https://cloud.google.com/python/django/run
* Enable service 
``` $ gcloud services enable sqladmin.googleapis.com ```
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
<!-- * Enable google cloud storage
gcloud enable storage-component.googleapis.com storage-api.googleapis.com storage.googleapis.com  -->
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

```$ gcloud services enable alloydb.googleapis.com compute.googleapis.com cloudresourcemanager.googleapis.com servicenetworking.googleapis.com```
* Add sidecar yaml
* set up private network for AlloyDB
<!-- gcloud compute addresses create default-private \
    --global \
    --purpose=VPC_PEERING \
    --prefix-length=20 \
    --network=projects/pdcp-cloud-014-lilakelland/global/networks/default -->

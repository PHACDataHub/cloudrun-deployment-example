# Cloudrun Deployment Example
[![CI Workflow - Code check on Pull Request](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/ci.yaml/badge.svg)](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/ci.yaml&cachebust=2)
[![CI/CD Workflow - Deploy to Cloud Run on Push to Main](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/build_deploy_cloudrun.yaml/badge.svg)](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/build_deploy_cloudrun.yaml.yaml&cachebust=2)

Working towards deploying Django apps to Google Cloud Run using AlloyDB (via auth proxy sidecar) and GitHub Actions.

*Work in progress - determining a workflow using a hello-world app and postgres-like db, then will apply to a more applicable projects*

## Currently running on
https://hello-world-app-65z3ddbfoa-nn.a.run.app/hello/

## Deployment options
1. GitHub Actions to run tests on pull request, then on push to main, a cloud build trigger will run steps to build the docker image, push to image artifact registry and deploy to cloud run (current way discribed below)
2. Capture the whole CI/CD process with GitHub Actions (now working on)

## Steps to deploy (with Cloud Build trigger)
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

Login to gcloud and set project

```$ gcloud auth login```

```$ gcloud config set project phx-hellodjango```

Set environment variables (change to your project's values)

``` 
export PROJECT_ID="phx-hellodjango" \
export REGION="northamerica-northeast1" \
export ARTIFACT_REGISTRY_REPO_NAME="hello-world-app" \
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
```

### 4. Add Image to Artifact Registry
1. Enable Artifact Registry

```$ gcloud services enable artifactregistry.googleapis.com```

2. Create repo 
``` 
gcloud artifacts repositories create ${ARTIFACT_REGISTRY_REPO_NAME} \
   --repository-format=docker \
   --location=${REGION} \
   --description=${ARTIFACT_REGISTRY_REPO_NAME}
```

<!-- c. give service account permission to read from repo
gcloud artifacts repositories add-iam-policy-binding ${ARTIFACT_REGISTRY_REPO_NAME} \
    --location=${REGION} \
    --member=serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com \
    --role="roles/artifactregistry.reader" -->

4. Authorize docker to push images to artifact registry

```$ gcloud auth configure-docker ${REGION}-docker.pkg.dev``` 

<!-- *not sure if we need to do this if deploying through cloud build triggers* -->
<!-- * Authorize docker to push images to artifact registry 
```$ gcloud auth configure-docker ```
* build and push image to registry
    ``` $ docker-compose build  ```
    ```$ docker-compose push ```  -->

*Turn on vunerability scanning in the gui!*

### 5. Set up Cloud Build 
a. Enable Cloud Build service

```$ gcloud services enable cloudbuild.googleapis.com```

b. Add [cloudbuild.yaml](cloudbuild.yaml) file to GitHub repository to indicate steps to deployment when triggered (test, lint, build Docker image, push to Artifact Registry, run on cloud Run)

c. Add cloud build trigger (this is set to be triggered on push to main branch)
```$ gcloud builds triggers create github \
  --name=hello-world-deploy-trigger \
  --region ${REGION} \
  --repo-name=cloudrun-deployment-example \
  --repo-owner=PHACDataHub \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --include-logs-with-status \
  --no-require-approval
  ```

### 6. Set up Cloud Run 
* Enable Cloud Run Service 
    ```$ gcloud services enable run.googleapis.com ```

    gcloud projects add-iam-policy-binding $PROJECT_ID --member=USER_OR_SERVICE_ACCOUNT_EMAIL --role=roles/run.viewer

### 7.Set up Database
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

### 8. Cloud Storage bucket
<!-- * Enable google cloud storage
gcloud enable storage-component.googleapis.com storage-api.googleapis.com storage.googleapis.com  -->
* Make bucket (needed to store .env?)
gsutil mb -l $REGION gs://$PROJECT_ID/django_bucket

### 9. Secret Manager
add username and password to bucket as .env
```
echo DATABASE_URL=postgres://postgres_username:postgres_password@//cloudsql/$PROJECT_ID:$REGION:hello-world-sql-instance/hello-world-db > .env
echo GS_BUCKET_NAME=$PROJECT_ID/django_bucket >> .env
echo SECRET_KEY=$(cat /dev/urandom | LC_ALL=C tr -dc '[:alpha:]'| fold -w 50 | head -n1) >> .env
```
### AlloyDB
* Activate (for this we need AlloyDB, Compute Engine, Resource Manager and Service Networking APIs)

```$ gcloud services enable alloydb.googleapis.com compute.googleapis.com cloudresourcemanager.googleapis.com servicenetworking.googleapis.com```
* Add sidecar yaml
* set up private network for AlloyDB
<!-- gcloud compute addresses create default-private \
    --global \
    --purpose=VPC_PEERING \
    --prefix-length=20 \
    --network=projects/pdcp-cloud-014-lilakelland/global/networks/default -->


### TODO 
-[] Database
-[] Run tests in CI (github actions or in cloud build yaml)
-[] Automate/ determine gcloud command for turning on vunerability scanning for Artifact Registry
-[X] Github actions (or somehting to reflect errors without going into cloud build to see - have writeback into repor set
-[] secret management (https://cloud.google.com/secret-manager/docs/quickstart)
-[] Learn if projects are using pdm or requirements.txt/ venvs are being used for patterns
-[] Automate approved hosts
-[] Dependabot (autocommit PR with workflow - but also should indicate some versions requirements.txt)
-[] Add [AlloyDB container](https://cloud.google.com/alloydb/docs/omni/install#install) to docker-compose to run locally a be able to test migrations
-[] Figure out migrations (look at [cloudmigrate.yaml](https://cloud.google.com/python/django/run#:~:text=The%20cloudmigrate.yaml%20file%20performs) or [buildpacks](https://cloud.google.com/blog/topics/developers-practitioners/running-database-migrations-cloud-run-jobs) )


#### Run tests (locally)
(in django project directory)

``` python manage.py test hello_world ```

### Resources:
* https://cloud.google.com/python/django/run
* https://github.com/google-github-actions/deploy-cloudrun
* https://phac-garden.vercel.app/other/cloudsql
* https://cloud.google.com/alloydb
* https://cloud.google.com/run/docs/deploying#sidecars


CICD options (TODO - add in testing and linting steps)
* [Cloud Build Trigger](https://cloud.google.com/run/docs/quickstarts/deploy-continuously)(this is the way here at the moment)
* https://github.com/google-github-actions/deploy-cloudrun
* https://github.com/marketplace/google-cloud-build - looks interesting! (but costs some cents)

Database options (AlloyDB)
* [Containerized](https://cloud.google.com/alloydb/docs/omni/install#install)
* GCP managed
To look at:
* https://github.com/GoogleCloudPlatform/alloydb-auth-proxy
* https://cloud.google.com/alloydb/docs/quickstart/integrate-cloud-run#configure_sample_app
* https://cloud.google.com/sql/docs/postgres/connect-instance-cloud-run
* https://cloud.google.com/sql/docs/mysql/connect-run
* https://cloud.google.com/sql/docs/mysql/connect-run#private-ip
* https://cloud.google.com/alloydb#section-5


* AlloyDB Omni (containerized)
    * https://cloud.google.com/alloydb/docs/omni/install#install

* https://codelabs.developers.google.com/create-alloydb-database-with-cloud-run-job

* https://www.cloudskillsboost.google/course_sessions/3132244/labs/339626

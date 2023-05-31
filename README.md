# Cloudrun Deployment Example
Working towards deploying Django apps to Google Cloud Run using AlloyDB (via auth proxy sidecar) and GitHub Actions.

*Work in progress - determining a workflow using a hello-world app and postgres-like db, then will apply to a more applicable projects*

## Currently running on 
https://hello-world-app-65z3ddbfoa-nn.a.run.app/hello/

## Steps to deploy
### Build app
* Using a django app here as an example
* Add tests - key component of ensuring no breaking changes with continuous deployment

* Set up DNS and add to approved hosts (in settings.py) if using Django

### Containerize 
* Add Dockerfile and requirement.txt to django project folder, if would like to run locally, create docker-compose.yaml to root.

To run locally:

```$ docker-compose up -d ```

```$ docker-compose down ``` to tear down at end

### Authenticate GCP
Login to gcloud and set project

```$ gcloud auth login```

```$ gcloud config set project phx-hellodjango```

Set environment variables

``` 
export PROJECT_ID="phx-hellodjango" \
export REGION="northamerica-northeast1" \
export ARTIFACT_REGISTRY_REPO_NAME="hello-world-app" \
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
```

### Artifact Registry
1. Activate Artifact Registry

```$ gcloud services enable artifactregistry.googleapis.com```

2. Create repo
``` 
gcloud artifacts repositories create ${ARTIFACT_REGISTRY_REPO_NAME} \
   --repository-format=docker \
   --location=${REGION} \
   --description=${ARTIFACT_REGISTRY_REPO_NAME}
```
3. Allow service account to read from the Artifact Registry
```
gcloud artifacts repositories add-iam-policy-binding ${ARTIFACT_REGISTRY_REPO_NAME} \
    --location=${REGION} \
    --member=serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com \
    --role="roles/artifactregistry.reader"
```
4. Authorize docker to push images to artifact registry

```$ gcloud auth configure-docker ${REGION}-docker.pkg.dev``` 

*not sure if we need to do this if deploying through cloud build triggers*
<!-- * Authorize docker to push images to artifact registry 
```$ gcloud auth configure-docker ```
* build and push image to registry
    ``` $ docker-compose build  ```
    ```$ docker-compose push ```  -->

*Turn on vunerability scanning in the gui!*

### Cloud Build
1. Activate

```$ gcloud services enable cloudbuild.googleapis.com```

2. Add cloud build trigger
```$ gcloud builds triggers create github \
  --name=hello-world-deploy-trigger \
  --region ${REGION} \
  --repo-name=cloudrun-deployment-example \
  --repo-owner=PHACDataHub \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml 
  ```
### Cloud Run 
* Activate 
    ```$ gcloud services enable run.googleapis.com ```
* Create Service
~gcloud run deploy testing-service --image northamerica-northeast1-docker.pkg.dev/phx-hellodjango/hello-world-app --region $REGION --allow-unauthenticated~ (defined in cloudbuild.yaml)
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
* Database
* Run tests in CI
* Github actions (or somehting to reflect errors without going into cloud build to see)
* secret management
* Apply to exisiting PHAC project
* change to pdm and add requirements. learn how these are being built - venvs or pdm
* Automate approved hosts

#### Run tests (locally)
(in django project directory)

``` python manage.py test hello_world ```

Resources:
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

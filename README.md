# Cloudrun Deployment Example
Deploying Django apps to Google Cloud Run using AlloyDB (via auth proxy sidecar) and GitHub Actions.

*Work in progress - figuring out the workflow first with a hello-world app with postgres-like db, then will apply to a more applicable example*


Resources:
* https://github.com/google-github-actions/deploy-cloudrun
* https://phac-garden.vercel.app/other/cloudsql
* https://cloud.google.com/alloydb
* https://cloud.google.com/run/docs/deploying#sidecars
https://cloud.google.com/run/docs/quickstarts/deploy-continuously* 

Steps 
* Build app
* Add tests
* Containerize (add Dockerfile and requirement.txt to django project folder, create docker-compose.yaml to root)
* (in django project, can build with: 
    * ``` docker build -t hello_world .```
    * ``` docker run -p 8000:8000 hello_world ```

or from root 
    * ``` docker-compose up -d ```
    * ``` docker-compose down ``` to tear down at end

* Activate Artifact Registry
    ```$ gcloud services enable artifactregistry.googleapis.com``

* Create artifact repo
export PROJECT_ID="pdcp-cloud-014-lilakelland" \
export REGION="northamerica-northeast1" \
export ARTIFACT_REGISTRY_REPO_NAME="hello-world-app" \

gcloud artifacts repositories create ${ARTIFACT_REGISTRY_REPO_NAME} \
   --repository-format=docker \
   --location=${REGION} \
   --description="${ARTIFACT_REGISTRY_REPO_NAME}"

* auth docker to push to artifact registry
```$ gcloud auth configure-docker ```

**** Add to Artifact Registry (turn on vunerability scanning) and add tag eg :latest or my-image@sha...)

*Note This requires the Artifact Registry API to be enabled. Furthermore, the deploying service account must have the Cloud Build Service Account role. The initial deployment will create an Artifact Registry repository which requires the Artifact Registry Admin role. (from https://github.com/marketplace/actions/deploy-to-cloud-run)*

* Activate cloud run
    ```$ gcloud services enable run.googleapis.com ``
* Add sidecar yaml

Next steps 
* add secrets
* modify to connect to db (or fork an existing project and use in this example)

### To Run 
``` $ cd djangoproject ```
``` $ python manage.py runserver ```

### Run tests
(in django project directory)
``` python manage.py test hello_world ```

TODO - change to pdm and add requirements. 
learn how these are being built - venvs or pdm
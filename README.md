# Cloudrun Deployment Example
Deploying Django apps to Google Cloud Run using AlloyDB (via auth proxy sidecar) and GitHub Actions.

*Work in progress - figuring out the workflow first with a hello-world app with postgres-like db, then will apply to a more applicable example*


Resources:
* https://github.com/google-github-actions/deploy-cloudrun
* https://phac-garden.vercel.app/other/cloudsql
* https://cloud.google.com/alloydb
* https://cloud.google.com/run/docs/deploying#sidecars
* https://cloud.google.com/run/docs/quickstarts/deploy-continuously 

* https://github.com/GoogleCloudPlatform/alloydb-auth-proxy
* https://cloud.google.com/sql/docs/postgres/connect-instance-cloud-run
* https://cloud.google.com/sql/docs/mysql/connect-run
* https://cloud.google.com/sql/docs/mysql/connect-run#private-ip

* https://codelabs.developers.google.com/create-alloydb-database-with-cloud-run-job


Steps 
* Build app
* Add tests
* Containerize (add Dockerfile and requirement.txt to django project folder, create docker-compose.yaml to root)
    * to run locally:
    * ``` docker-compose up -d ```
    * ``` docker-compose down ``` to tear down at end

* Activate Artifact Registry
    ```$ gcloud services enable artifactregistry.googleapis.com``

* Create artifact repo
    * Set environment variables
    ``` export PROJECT_ID="phx-hellodjango" \
        export REGION="northamerica-northeast1" \
        export ARTIFACT_REGISTRY_REPO_NAME="hello-world-app" ```

    Create repo
    ``` gcloud artifacts repositories create ${ARTIFACT_REGISTRY_REPO_NAME} \
    --repository-format=docker \
    --location=${REGION} \
    --description="${ARTIFACT_REGISTRY_REPO_NAME}" ```

    *Turn on vunerability scanning in the gui!*

* Authorize docker to push images to artifact registry
```$ gcloud auth configure-docker ```
    * build and push image to registry
    ``` $ docker-compose build  ```
    ```$ docker-compose push ```

* Activate cloud run
    ```$ gcloud services enable run.googleapis.com ``

* Add sidecar yaml

Next steps 
* add secrets
* AlloyDB
* Github actions with cloud run:

*   Set up permssions
    https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling

<!-- gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:service-71366405699@serverless-robot-prod.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountTokenCreator" --role="roles/run.admin"   --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID   --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com"   --role="roles/run.admin"   --role="roles/iam.serviceAccountUser" --role="roles/iam.serviceAccountTokenCreator" -->

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/run.serviceAgent" \
  --condition=None
<!-- export PROJECT_ID="phx-hellodjango"
export GITHUB_REPO_NAME="cloudrun-deployment-example"

gcloud builds triggers create github \
  --name=test-site-nginx-001 \
  --region ${REGION} \
  --repo-name=${GITHUB_REPO_NAME} \
  --repo-owner=daneroo \
  --branch-pattern="^main$" \
  --build-config=apps/site-nginx/cloudbuild.yaml -->

* Apply to exisiting PHAC project

### Run tests
(in django project directory)
``` python manage.py test hello_world ```

TODO - change to pdm and add requirements. 
learn how these are being built - venvs or pdm
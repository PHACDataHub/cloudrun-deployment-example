# Cloudrun Deployment Example
Deploying Django apps to Google Cloud Run using AlloyDB (via auth proxy sidecar) and GitHub Actions.

*Work in progress - figuring out the workflow first with a hello-world app with postgres-like db, then will apply to a more applicable example*

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

Running @ https://hello-world-app-65z3ddbfoa-nn.a.run.app/hello/

Steps 
* Build app
* Add tests

* Set up DNS and add to approved hosts (in settings.py) if using Django

* Containerize (add Dockerfile and requirement.txt to django project folder, create docker-compose.yaml to root)
    * to run locally:
    * ``` docker-compose up -d ```
    * ``` docker-compose down ``` to tear down at end

* Activate Artifact Registry
    ```$ gcloud services enable artifactregistry.googleapis.com``

* Create Artifact Registry Repo:
    1. Set environment variables
    ``` export PROJECT_ID="phx-hellodjango" \
        export REGION="northamerica-northeast1" \
        export ARTIFACT_REGISTRY_REPO_NAME="hello-world-app" 
    ```
    2. Create repo
    ``` gcloud artifacts repositories create ${ARTIFACT_REGISTRY_REPO_NAME} \
    --repository-format=docker \
    --location=${REGION} \
    --description="${ARTIFACT_REGISTRY_REPO_NAME}" 
    ```

    *Turn on vunerability scanning in the gui!*

* Authorize docker to push images to artifact registry *not sure if we need to do this if not using locally*
```$ gcloud auth configure-docker ```
* build and push image to registry
    ``` $ docker-compose build  ```
    ```$ docker-compose push ```

* Activate cloud build
* Add cloud build trigger

gcloud builds triggers create github \
  --name=hello-world-deploy-trigger \
  --region ${REGION} \
  --repo-name=cloudrun-deployment-example \
  --repo-owner=PHACDataHub \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml 

* Activate cloud run
    ```$ gcloud services enable run.googleapis.com ``
    <!-- * Add permissions ``` gcloud projects add-iam-policy-binding pdcp-cloud-014-lilakelland --member=serviceAccount:294163875507@cloudbuild.gserviceaccount.com --role=roles/run.viewer ``` -->

* Connect Cloud Run (build?) to repo (console)

* set up private network for AlloyDB
gcloud compute addresses create default-private \
    --global \
    --purpose=VPC_PEERING \
    --prefix-length=20 \
    --network=projects/pdcp-cloud-014-lilakelland/global/networks/default

* AlloyDB
    * set up permissions roles/alloydb.client
    * Enable the AlloyDB, Compute Engine, and Resource Manager APIs. Enable Service Networking API

* Add sidecar yaml

Next steps 
* add secrets

* Github actions with cloud run:

*   Set up permssions
    https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling

<!-- gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:service-71366405699@serverless-robot-prod.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountTokenCreator" --role="roles/run.admin"   --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID   --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com"   --role="roles/run.admin"   --role="roles/iam.serviceAccountUser" --role="roles/iam.serviceAccountTokenCreator" -->

<!-- gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/run.serviceAgent" \
  --condition=None

  gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:71366405699@cloudbuild.gserviceaccount.com --role=roles/storage.objectViewer -->

<!-- #### Deploy to cloud run
gcloud run deploy testing-service --image northamerica-northeast1-docker.pkg.dev/phx-hellodjango/hello-world-app --region $REGION --allow-unauthenticated -->
<!-- 
ERROR: (gcloud.run.deploy) User [lila.kelland@gcp.hc-sc.gc.ca] does not have permission to access namespaces instance [phx-hellodjango] (or it may not exist): Google Cloud Run Service Agent does not have permission to get access tokens for the service account 71366405699-compute@developer.gserviceaccount.com. Please give service-71366405699@serverless-robot-prod.iam.gserviceaccount.com permission iam.serviceAccounts.getAccessToken on the service account. Alternatively, if the service account is unspecified or in the same project you are deploying in, ensure that the Service Agent is assigned the Google Cloud Run Service Agent role roles/run.serviceAgent. -->


<!-- 
gcloud builds triggers create github \
  --name=test-site-nginx-001 \
  --region ${REGION} \
  --repo-name=${GITHUB_REPO_NAME} \
  --repo-owner=daneroo \
  --branch-pattern="^main$" \
  --build-config=apps/site-nginx/cloudbuild.yaml --> -->

* Apply to exisiting PHAC project

### Run tests
(in django project directory)
``` python manage.py test hello_world ```

TODO - change to pdm and add requirements. 
learn how these are being built - venvs or pdm
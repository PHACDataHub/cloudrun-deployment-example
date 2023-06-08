## Deploy using [Cloud Build Trigger](https://cloud.google.com/sdk/gcloud/reference/beta/builds/triggers/create/github)
*Start with steps 1-4 outlined in [deployment-instructions/README.md](README.md)*

### i. Artifact Registry
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

```
  $ gcloud auth configure-docker ${REGION}-docker.pkg.dev
  ``` 

<!-- *not sure if we need to do this if deploying through cloud build triggers* -->
<!-- * Authorize docker to push images to artifact registry 
```$ gcloud auth configure-docker ```
* build and push image to registry
    ``` $ docker-compose build  ```
    ```$ docker-compose push ```  -->

*Turn on vunerability scanning in the gui!*

### ii. Set up Cloud Build  (https://cloud.google.com/sdk/gcloud/reference/beta/builds/triggers/create/github)
1. Enable Cloud Build service and source repo

```$ gcloud services enable cloudbuild.googleapis.com sourcerepo.googleapis.com```


2. Add [cloudbuild.yaml](djangoproject/cloudbuild.yaml) file, to the Django project folder, to indicate steps to deployment when triggered (test, lint, build Docker image, push to Artifact Registry, run on cloud Run)

3. Connect repo with cloud build (doesn't appear to be gcloud option to do this)
https://cloud.google.com/build/docs/automating-builds/github/connect-repo-github?generation=1st-gen


4. Add cloud build trigger (this is set to be triggered on push to main branch)
```
gcloud builds triggers create github \
  --name=hello-world-deploy-trigger \
  --region ${REGION} \
  --repo-name=cloudrun-deployment-example \
  --repo-owner=PHACDataHub \
  --branch-pattern="^main$" \
  --build-config=djangoproject/cloudbuild.yaml \
  --include-logs-with-status \
  --no-require-approval
  ```
  
### iii. Set up Cloud Run 
* Enable Cloud Run Service 
    ```
    $ gcloud services enable run.googleapis.com
     ```

* Bind permissions for cloud build to push to cloud run 
** change out project number 
  ```
  gcloud projects describe PROJECT_ID --format="value(projectNumber)" 
  ```

  ```
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:249044526600@cloudbuild.gserviceaccount.com \
    --role=roles/run.admin
  ```

  ```
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:249044526600@cloudbuild.gserviceaccount.com \
    --role=roles/iam.serviceAccountUser
  ```


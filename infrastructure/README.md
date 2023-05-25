### Okay, not really infrastructure....

Just recording how set-up in GCP (Keith feel free to wipe this out with your infra magic!)
Following along with https://phac-garden.vercel.app/

Create Artifact Registry
# so we can execute gcloud commands
gcloud auth login

 
 # TODO TURN ON VULNERABILITY SCANNING!! 
# project name # Get the PROJECT_NUMBER from the PROJECT_ID
export PROJECT_ID="pdcp-cloud-014-lilakelland" 
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
export REGION="northamerica-northeast1" 
export ARTIFACT_REGISTRY_REPO_NAME="hello-world-app" 

# set to correct project
gcloud config set project ${PROJECT_ID}
 
# Create an artifact registry repository
gcloud artifacts repositories create ${ARTIFACT_REGISTRY_REPO_NAME} \
   --repository-format=docker \
   --location=${REGION} \
   --description="${ARTIFACT_REGISTRY_REPO_NAME}"
 
~~# Allow our service account to read from the registry
gcloud artifacts repositories add-iam-policy-binding ${ARTIFACT_REGISTRY_REPO_NAME} \
    --location=${REGION} \
    --member=serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com \
    --role="roles/artifactregistry.reader"~~

so this did not work for me, but...
``` gcloud projects set-iam-policy PROJECT /PATH/TO/policy.yaml ```
* from https://cloud.google.com/artifact-registry/docs/access-control#gcloud

seems to already be bound....(and seems to work)

allow docker to read write - was using cloud shell, need ot do this locally or where code is living
* ```$ gcloud auth configure-docker ${REGION}-docker.pkg.dev``
or gcloud auth configure-docker northamerica-northeast1-docker.pkg.dev since using montreal at the moment

* reconfigure yaml to point to GCP project  (add image line)

``` $ docker-compose build \ docker-compose push ```


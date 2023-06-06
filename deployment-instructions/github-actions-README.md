*need to clean up*

### Authenticate GCP
For the following steps you'll need the [gcloud](https://cloud.google.com/sdk/docs/install) (and maybe [gsutil](https://cloud.google.com/storage/docs/gsutil_install)) clis installed. 


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

### Enable APIs and Services 
Artifact registry to store container image used by cloud run
```
gcloud services enable \
artifactregistry.googleapis.com \
storage-component.googleapis.com \
storage-api.googleapis.com storage.googleapis.com \
cloudbuild.googleapis.com \
run.googleapis.com \
enable alloydb.googleapis.com compute.googleapis.com cloudresourcemanager.googleapis.com servicenetworking.googleapis.com
```
 **IAM Service Account Credentials API**

### Create Artifact Registry repo 
``` 
gcloud artifacts repositories create ${ARTIFACT_REGISTRY_REPO_NAME} \
   --repository-format=docker \
   --location=${REGION} \
   --description=${ARTIFACT_REGISTRY_REPO_NAME}
```
### Set up [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
Other references:
https://medium.com/google-cloud/how-does-the-gcp-workload-identity-federation-work-with-github-provider-a9397efd7158
https://gist.github.com/palewire/12c4b2b974ef735d22da7493cf7f4d37

#### Create workload identity federation pool
(note $REGION doesn't work here)

~export SERVICE_ACCOUNT=github-action \
export WORKLOAD_IDENTITY_POOL=github-wif-pool~

```
$ gcloud iam workload-identity-pools create github-wif-pool --location="global" --project $PROJECT_ID
```

#### Create workload Identity Provider
```
gcloud iam workload-identity-pools providers create-oidc githubwif \
--location="global" --workload-identity-pool="github-wif-pool"  \
--issuer-uri="https://token.actions.githubusercontent.com" \
--attribute-mapping="attribute.actor=assertion.actor,google.subject=assertion.sub,attribute.repository=assertion.repository" \
--project $PROJECT_ID
```

#### Create service account to bind permissions to (and use for workload identity)
<!-- gcloud iam service-accounts create github-action \
--display-name="Service account for github actions cloud run deploy used by WIF" \
--project $PROJECT_NUMBER -->
```
gcloud iam service-accounts create github-actions \
    --description="Service account for github actions cloud run deploy used by Workload identity federation" \
    --display-name="github actions service account"
```    

<!-- actually have service account github-action@pdcp-cloud-014-lilakelland.iam.gserviceaccount.com -->
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:github-actions@phx-01h1yptgmche7jcy01wzzpw2rf.iam.gserviceaccount.com" \
--role="roles/compute.viewer" \
--role="roles/owner"
```

check make sure working: 
```
gcloud projects get-iam-policy $PROJECT_ID  \
--flatten="bindings[].members" \
--format='table(bindings.role)' \
--filter="bindings.members:serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com"
```

```
gcloud iam service-accounts add-iam-policy-binding github-actions@$PROJECT_ID.iam.gserviceaccount.com \
--project=$PROJECT_ID \
--role="roles/iam.workloadIdentityUser" \
--member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-wif-pool/attribute.repository/PHACDataHub/cloudrun-deployment-example"
```

<!-- <!-- ## restrict to main  -->
<!-- :ref:refs/heads/main" -->
<!-- 
run service 
gcloud projects add-iam-policy-binding $PROJECT_ID --member="github-action@$PROJECT_ID.iam.gserviceaccount.com" --role=roles/run.admin --> -->

### Add yaml file in [.github/workflows](../.github/workflows/build_deploy_cloudrun.yaml)

When commit to main, workflow will initiate
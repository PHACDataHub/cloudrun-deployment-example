## Deploy using [GitHub Actions to Deploy to Cloud Run](https://github.com/google-github-actions/deploy-cloudrun)

*Start with steps 1-4 outlined in [deployment-instructions/README.md](README.md)*

QUESTION - should we pull out and docker build outside?

### i. Update settings.py
Add the following into [settings.py](../djangoproject/djangoproject/settings.py)

```
if os.getenv('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github-actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }
```

<!-- Set environment variables (change to your project's values)

``` 
export PROJECT_ID="phx-hellodjango" \
export REGION="northamerica-northeast1" \
export ARTIFACT_REGISTRY_REPO_NAME="hello-world-app" \
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
``` -->

### ii. Enable APIs and Services 

```
gcloud services enable \
    artifactregistry.googleapis.com \
    storage-component.googleapis.com \
    storage-api.googleapis.com \
    storage.googleapis.com \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    alloydb.googleapis.com \
    compute.googleapis.com \
    cloudresourcemanager.googleapis.com \
    servicenetworking.googleapis.com \
    iam.googleapis.com
```
(IAM - IAM Service Account Credentials AP - for impersonating Creates short-lived credentials for impersonating IAM service accounts, need both the Cloud Run Admin and Service Account User roles for cloud run )

*TODO - review list to make sure still need them all*

### iii. Create Artifact Registry repo 
``` 
gcloud artifacts repositories create ${ARTIFACT_REGISTRY_REPO_NAME} \
   --repository-format=docker \
   --location=${REGION} \
   --description=${ARTIFACT_REGISTRY_REPO_NAME}
```
### iv. Set up [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation) (for keyless authentication)
References:
* https://cloud.google.com/iam/docs/workload-identity-federation
* https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions
* https://medium.com/google-cloud/how-does-the-gcp-workload-identity-federation-work-with-github-provider-a9397efd7158
https://gist.github.com/palewire/12c4b2b974ef735d22da7493cf7f4d37

#### a) Create workload identity federation pool
(note $REGION doesn't work here - location is global)

~~export SERVICE_ACCOUNT=github-action \
export WORKLOAD_IDENTITY_POOL=github-wif-pool~~

```
$ gcloud iam workload-identity-pools create github-wif-pool --location="global" --project $PROJECT_ID
```

#### b) Create workload Identity Provider
```
gcloud iam workload-identity-pools providers create-oidc githubwif \
--location="global" --workload-identity-pool="github-wif-pool"  \
--issuer-uri="https://token.actions.githubusercontent.com" \
--attribute-mapping="attribute.actor=assertion.actor,google.subject=assertion.sub,attribute.repository=assertion.repository" \
--project $PROJECT_ID
```

#### c) Create service account to bind permissions to (and use for workload identity)
<!-- gcloud iam service-accounts create github-action \
--display-name="Service account for github actions cloud run deploy used by WIF" \
--project $PROJECT_NUMBER -->
```
gcloud iam service-accounts create github-actions \
    --description="Service account for github actions cloud run deploy used by Workload identity federation" \
    --display-name="github actions service account"
```    

#### d) Give GitHub service account permissions
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:github-actions@phx-01h1yptgmche7jcy01wzzpw2rf.iam.gserviceaccount.com" \
--role="roles/compute.viewer" \
--role="roles/owner"
```

#### e) Check make sure working: 
```
gcloud projects get-iam-policy $PROJECT_ID  \
--flatten="bindings[].members" \
--format='table(bindings.role)' \
--filter="bindings.members:serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com"
```
#### f) Associate with GitHub Repo
```
gcloud iam service-accounts add-iam-policy-binding github-actions@$PROJECT_ID.iam.gserviceaccount.com \
--project=$PROJECT_ID \
--role="roles/iam.workloadIdentityUser" \
--member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-wif-pool/attribute.repository/PHACDataHub/cloudrun-deployment-example"
```

*TODO add it time limitations*

### v. Add the GitHub Actions yaml file to deploy to Cloud Run in [.github/workflows](../.github/workflows/build_deploy_cloudrun.yaml) 
Use the workload identity federation option to authentication with GCP. 


Now when you commit to main, the workflow will initiate. 
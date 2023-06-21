# Cloud Run Django Deployment Example
[![CI Workflow - Code check on Pull Request](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/ci.yaml/badge.svg)](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/ci.yaml&cachebust=2)
[![CI/CD Workflow - Deploy to Cloud Run on Push to Main](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/build_deploy_cloudrun.yaml/badge.svg)](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/build_deploy_cloudrun.yaml.yaml&cachebust=2)

Working towards deploying Django apps to Google Cloud Run, using a Cloud SQL Postgres database and a Cloud Build GitHub Trigger for the continuous deployment.  (Also exploring Github actions push deployment as well as AlloyDB as Cloud SQL alternative)

*Work in progress - determining a workflow using a hello-world app and postgres-like db, then will apply to a more applicable projects*

## Currently running on
https://hello-world-vlfae7w5dq-nn.a.run.app/ (from GitHub Actions)
and https://hello-world-three-vlfae7w5dq-nn.a.run.app (from Cloud Build trigger).

## References: 
* Django app: https://docs.djangoproject.com/en/4.2/intro/tutorial01/
* Deployment: 
    * https://cloud.google.com/python/django/run 
    * https://github.com/daneroo/phac-epi-garden


## Ready Django App:
1. Build [app](./mydjangoproject/) with tests
2. Add requirements.txt to indicate dependencies 
3. Add a Dockerfile for containerization 
4. Add .dockerignore and .gitignore
5. Modify settings.py  (https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
* rename settings.py to basesettings.py
* add settings.py file from here (and link) to include Google Cloud deployment instructions and secrets
* change your app name in installed apps section of settings.py

## Steps to set up GCP Deployment
1. Authenticate 
    ```
    gcloud auth application-default login
    ```
2. Set project Variable
    ```
    gcloud config set project <your project>
    ```
3. Enable APIs and set up service accounts and secrets for Artifact Registry, Cloud Build trigger, Cloud Run and Cloud SQL.  Provision database. 
* Follow instructions in [deploy/gcp-initialization.sh](deploy/gcp-initialization.sh) (step by step in terminal or command prompt, or just run). 
*Note: variables need to be modified for your project.* 

* During first run through, when you're prompted with an error indication Cloud Build needs to be connected to the GitHub Repo:
    * Log into console to perform manual steps required for deployment set up
        * Cloud build connect to GitHub Repo
        * Artifact Registry - select 'Check for vunerabilities

* Then rerun.
<!-- (as django manages scaling up and down, we're using a lightweight version of python, and using a python based webserver - waitress, this elimates the need for some of the packages)   -->
## Cloud SQL Proxy (Before Cloud Deploy for intial migrations on the first go)
(for initial makemigrations)
1. Download [Cloud SQL Proxy](https://cloud.google.com/sql/docs/postgres/sql-proxy) 
This is for connecting to Cloud SQL from your computer for initial set up 
* [Link to curl command to download & install](https://cloud.google.com/sql/docs/postgres/sql-proxy#install)

    ```
    chmod +x cloud-sql-proxy 
    ```
* Run app locally with cloud sql proxy (note this is for non-windows machines)(https://cloud.google.com/sql/docs/sqlserver/connect-instance-auth-proxy) for other devices 
```
./cloud-sql-proxy $PROJECT_ID:$REGION:$INSTANCE_NAME
```
Note: This seems to timeout - if you get oauth2: "invalid_grant" "reauth related error (invalid_rapt):
```
gcloud auth application-default revoke
```
```
gcloud  auth application-default login
```
# run migrations
Change directories into <mydjangoproject>
```
python manage.py makemigrations
python manage.py makemigrations <app>
python manage.py migrate
<!-- python manage.py collectstatic -->
```

## Deploy


1. Manually Cloud Build with no trigger:
```
gcloud builds submit --config cloudbuild.yaml
```
2. Otherwise, the project is automatically deployed each time there's a commit to main branch


TODO - waitress and
TODO - ci.yaml github actions for pull request
## After first deployment
### Set Service URL
* After first deployment, set SERVICE_URL environment variable (replace 'hello-world' with your Cloud Run service name in both cases.)
* Retrieve URL (also displayed in Service Details page in Cloud Run)
``` 
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed \
    --region northamerica-northeast1 --format "value(status.url)")
 ``` 

 * Set CLOUDRUN_SERVICE_URL used in settings.py for CSRF and allowed hosts (otherwiser will have issues)
 ```
gcloud run services update $SERVICE_NAME \
    --platform managed \
    --region northamerica-northeast1 \
    --set-env-vars CLOUDRUN_SERVICE_URL=$SERVICE_URL
```
** note this step will change once we have the DNS set up 


## TO DO 
* GitHub Actions https://www.hacksoft.io/blog/github-actions-in-action-setting-up-django-and-postgres

* Determine when tests should run.  Currently, tests run on pull request can we also run these test prior to the Cloud Build (rather than concurently) on push to main? Or should we be locking downthe main branch so pull requests naturally always happen before push to main 
* Automate/ determine gcloud command for turning on vunerability scanning for Artifact Registry
* Connecting GitHub Repo to Cloud Build is also a manual step and requires someone's GitHub account for authorization - Keith is looking into other options/ possibilities
* Yakima account (Config Connector for ifrastucture as code set up (IaS) has a misleading name in the IAM console - change this to something more user friendly if we don't know what it is)
* Automate approved hosts (Dan got SSL working for DNS so may not need this?)
* Docker compose to use context (add deploy folder) & tests!!

<!-- 
#### Run tests (locally)
(in django project directory)

``` python manage.py test hello_world ``` -->

### Resources:
* https://phac-garden.vercel.app/other/cloudsql
* https://cloud.google.com/python/django/run
* https://github.com/google-github-actions/deploy-cloudrun
* https://cloud.google.com/alloydb
* https://cloud.google.com/run/docs/deploying#sidecars
* https://cloud.google.com/blog/products/serverless/cloud-run-now-supports-multi-container-deployments
* https://cloud.google.com/sql/docs/postgres/connect-auth-proxy#expandable-1 
* secret management (https://cloud.google.com/secret-manager/docs/quickstart


CICD options (TODO - add in testing and linting steps)
* [Cloud Build Trigger](https://cloud.google.com/run/docs/quickstarts/deploy-continuously)
* [GitHub Actions for Deploy to Cloud Run](https://github.com/google-github-actions/deploy-cloudrun)

videos 
* https://www.youtube.com/watch?v=cBrn5IM4mA8&t=436s
* https://www.youtube.com/watch?v=rebyg9_eTHM
* [cloud Run + Cloud SQL set up](https://www.youtube.com/watch?v=cBrn5IM4mA8[])

Database 

To look at:
* https://github.com/GoogleCloudPlatform/alloydb-auth-proxy
* https://cloud.google.com/alloydb/docs/quickstart/integrate-cloud-run#configure_sample_app
* https://cloud.google.com/sql/docs/postgres/connect-instance-cloud-run
* https://cloud.google.com/sql/docs/mysql/connect-run
* https://cloud.google.com/sql/docs/mysql/connect-run#private-ip
* https://cloud.google.com/alloydb#section-5
* https://github.com/GoogleCloudPlatform/cloud-sql-proxy
* [Cloud SQL Auth Proxy](https://cloud.google.com/python/django/run) modify for postgres then AlloyDB
* [Cloud SQL Connector](https://cloud.google.com/sql/docs/mysql/connect-connectors)
* https://cloud.google.com/alloydb/docs/auth-proxy/overview
* https://github.com/GoogleCloudPlatform/alloydb-go-connector


AlloyDB Omni (containerized version - for testing)
* https://cloud.google.com/alloydb/docs/omni/install#install
* https://codelabs.developers.google.com/create-alloydb-database-with-cloud-run-job
* https://www.cloudskillsboost.google/course_sessions/3132244/labs/339626


Migrations:
* https://cloud.google.com/blog/topics/developers-practitioners/running-database-migrations-cloud-run-jobs
* [cloudmigrate.yaml](https://cloud.google.com/python/django/run#:~:text=The%20cloudmigrate.yaml%20file%20performs)
* https://cloud.google.com/blog/topics/developers-practitioners/running-database-migrations-cloud-run-jobs

Options: 
* run from local computer with Auth proxy
* run as part of build process 
https://cloud.google.com/run/docs/managing/jobs

gcloud run jobs update JOB_NAME --image IMAGE_URL

# Cloud Run Django Deployment Example
[![CI Workflow - Code check on Pull Request](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/ci.yaml/badge.svg)](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/ci.yaml&cachebust=2)
[![CI/CD Workflow - Deploy to Cloud Run on Push to Main](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/build_deploy_cloudrun.yaml/badge.svg)](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/build_deploy_cloudrun.yaml.yaml&cachebust=2)

Working towards deploying Django apps to Google Cloud Run using AlloyDB (via auth proxy sidecar) and GitHub Actions (or Cloud Build).

*Work in progress - determining a workflow using a hello-world app and postgres-like db, then will apply to a more applicable projects*

## Currently running on
https://hello-world-vlfae7w5dq-nn.a.run.app/ (from GitHub Actions)
and https://hello-world-from-cloud-build-trigger-vlfae7w5dq-nn.a.run.app/ (from Cloud Build trigger).

## Deployment options
1. GitHub Actions to run tests on a new Pull Request.  On a push to the main branch, a Cloud Build trigger will run through the steps outlined in [cloudbuild.yaml](./cloudbuild.yaml) to build the docker image, push to the image Artifact Registry and then deploy to Cloud Run (Cloud Run can only be deployed to from the Artifact Registry).

2. Capture the whole CI/CD process with GitHub Actions using [keyless authentication](https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions). Dan brought up a great question - right now it's building the image with GCP, why not pull the build and push steps out of google cloud and only do the deploy to Cloud Run step with GCP.

Both of these are running at the moment, but sounds like we're leaning towards the Cloud Build trigger option as it's more inline with pull based Zero Trust model.

## Status 
Working towards connecting the database instance with Cloud Run instance.  
#### 1. Socket
Dan has a [way that works](https://github.com/daneroo/phac-epi-garden/tree/main), but we're still struggling to get it up and running with Django.  This method connects to a local socket in the Cloud Run container that Google will 'magic-black-box' connect to  Cloud SQL (similar to [this](https://youtu.be/cBrn5IM4mA8?t=430).)
* Pros - it works (well almost works here)
* Cons - it uses a public IP address (with an empty whitelist), but may not be ideal in production. 

#### 2. Auth Proxy 
John's been working on the Auth Proxy method - and has it working for a [wagtail deployment](https://wagtail-cloudrun-vlfae7w5dq-uc.a.run.app/). Next is moving towards implimenting this as a sidecar for continuous deployment. 



Deployment instructions (work in progress as we iron out the details), are found in the [deploy folder](./deploy/), along with associated yaml and shell scripts capture the gcloud commands for set up.  


### TODO (clean this up and/or turn into repo issues)

* Determine when tests should run.  Currently, tests run on pull request can we also run these test prior to the Cloud Build (rather than concurently) on push to main? Or should we be locking downthe main branch so pull requests naturally always happen before push to main 
* Automate/ determine gcloud command for turning on vunerability scanning for Artifact Registry
* Connecting GitHub Repo to Cloud Build is also a manual step and requires someone's GitHub account for authorization - Keith is looking into other options/ possibilities
* Yakima account (Config Connector for ifrastucture as code set up (IaS) has a misleading name in the IAM console - change this to something more user friendly if we don't know what it is)
* Automate approved hosts (Dan got SSL working for DNS so may not need this?)


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

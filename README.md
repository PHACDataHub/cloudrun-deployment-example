# Cloudrun Deployment Example
[![CI Workflow - Code check on Pull Request](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/ci.yaml/badge.svg)](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/ci.yaml&cachebust=2)
[![CI/CD Workflow - Deploy to Cloud Run on Push to Main](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/build_deploy_cloudrun.yaml/badge.svg)](https://github.com/PHACDataHub/cloudrun-deployment-example/actions/workflows/build_deploy_cloudrun.yaml.yaml&cachebust=2)

Working towards deploying Django apps to Google Cloud Run using AlloyDB (via auth proxy sidecar) and GitHub Actions.

*Work in progress - determining a workflow using a hello-world app and postgres-like db, then will apply to a more applicable projects*

## Currently running on
https://hello-world-app-65z3ddbfoa-nn.a.run.app/hello/

## Deployment options
1. GitHub Actions to run tests on pull request, then on push to main, a cloud build trigger will run steps to build the docker image, push to image artifact registry and deploy to cloud run (working currently)
2. Capture the whole CI/CD process with GitHub Actions (now working on)

### TODO 
-[] Database
-[] Run tests in CI (github actions or in cloud build yaml)
-[] Automate/ determine gcloud command for turning on vunerability scanning for Artifact Registry
-[] Github actions (update to use Workload identity federation) (https://gist.github.com/palewire/12c4b2b974ef735d22da7493cf7f4d37)
-[] secret management (https://cloud.google.com/secret-manager/docs/quickstart)
-[] Learn if projects are using pdm or requirements.txt/ venvs are being used for patterns
-[] Automate approved hosts
-[] Dependabot (autocommit PR with workflow - but also should indicate some versions requirements.txt)
-[] Add [AlloyDB container](https://cloud.google.com/alloydb/docs/omni/install#install) to docker-compose to run locally a be able to test migrations
-[] Figure out migrations (look at [cloudmigrate.yaml](https://cloud.google.com/python/django/run#:~:text=The%20cloudmigrate.yaml%20file%20performs) or [buildpacks](https://cloud.google.com/blog/topics/developers-practitioners/running-database-migrations-cloud-run-jobs) )


#### Run tests (locally)
(in django project directory)

``` python manage.py test hello_world ```

### Resources:
* https://cloud.google.com/python/django/run
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




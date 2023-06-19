# https://cloud.google.com/sql/docs/postgres/connect-run
# export PROJECT_ID=$(gcloud config get-value project) 
# export SERVICE_NAME=hello-world
# export REGION=northamerica-northeast1
export INSTANCE_NAME=test-instance
PROJECT_ID=$(gcloud config get-value project) 
SERVICE_NAME=hello-world
REGION=northamerica-northeast1
INSTANCE_NAME=test-instance #Cloud SQL instance
SERVICE_NAME=hello-world-two #Cloud run
SECRET_SETTINGS_NAME=django_settings
ARTIFACT_REGISTRY_REPO=hello-world-app
DB_NAME=test-db
DB_USER=test-user
DB_PASSWORD=password123


# Create Postgres instance
gcloud sql instances create ${INSTANCE_NAME} \
    --project ${PROJECT_ID} \
    --database-version POSTGRES_14 \
    --tier db-f1-micro \
    --region ${REGION}

# create db
gcloud sql databases create ${DB_NAME} \
    --instance ${INSTANCE_NAME}

#create user
gcloud sql users create ${DB_USER} \
    --instance ${INSTANCE_NAME} \
    --password ${DB_PASSWORD}

# create storage bucket
gsutil mb -l ${REGION}  gs://${PROJECT_ID}_MEDIA_BUCKET

# create secrets
echo DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@//cloudsql/{PROJECT_ID}:${REGION}:${INSTANCE_NAME}/${DB_NAME} > .env
echo GS_BUCKET_NAME=${PROJECT_ID}_MEDIA_BUCKET >> .env
echo SECRET_KEY=$(cat /dev/urandom | LC_ALL=C tr -dc '[:alpha:]'| fold -w 50 | head -n1) >> .env

# store secrets
gcloud secrets create --locations ${REGION} --replication-policy user-managed ${SECRET_SETTINGS_NAME} --data-file .env

# OR UPDATE
gcloud secrets versions add ${SECRET_SETTINGS_NAME} \
    --data-file=.env \
    --project=${PROJECT_ID}

# chek that they are there 
gcloud secrets describe ${SECRET_SETTINGS_NAME}

gcloud secrets versions access latest --secret ${SECRET_SETTINGS_NAME}  #django_settings

# get project number 
gcloud projects describe $PROJECT_ID --format='value(projectNumber)'

# cloud run service secret access
gcloud secrets add-iam-policy-binding ${SECRET_SETTINGS_NAME} \
    --member serviceAccount:249044526600-compute@developer.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor

# secret access to cloud build 
gcloud secrets add-iam-policy-binding ${SECRET_SETTINGS_NAME} \
    --member serviceAccount:249044526600@cloudbuild.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor

#create super for  user password
echo -n "$(cat /dev/urandom | LC_ALL=C tr -dc '[:alpha:]'| fold -w 30 | head -n1)" | gcloud secrets create --locations ${REGION} --replication-policy user-managed superuser_password --data-file -

# give cloud build access to this superuser password
gcloud secrets add-iam-policy-binding superuser_password \
    --member serviceAccount:249044526600@cloudbuild.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor

# cloud build to sql access 
gcloud projects add-iam-policy-binding phx-01h1yptgmche7jcy01wzzpw2rf \
    --member serviceAccount:249044526600@cloudbuild.gserviceaccount.com \
    --role roles/cloudsql.client

# run locally
./cloud-sql-proxy ${PROJECT_ID}:${REGION}:${INSTANCE_NAME}

# in another terminal 
export GOOGLE_CLOUD_PROJECT=phx-01h1yptgmche7jcy01wzzpw2rf
export USE_CLOUD_SQL_AUTH_PROXY=true

# run migrations
python manage.py makemigrations
python manage.py makemigrations polls
python manage.py migrate
<!-- python manage.py collectstatic -->

# can locally connect python manage.py runserver

# deploy cloud build, run database migrations and populate static assests
gcloud builds submit --config cloudbuild.yaml \
    --substitutions _INSTANCE_NAME=test-instance, _REGION=northamerica-northeast1

deploy cloud run 
gcloud run deploy polls-service \
    --platform managed \
    --region northamerica-northeast1 \
    --image gcr.io/phx-01h1yptgmche7jcy01wzzpw2rf/polls-service \
    --add-cloudsql-instances phx-01h1yptgmche7jcy01wzzpw2rf:northamerica-northeast1:test-instance \
    --allow-unauthenticated


save service url as environment variable
<!-- SERVICE_URL=$(gcloud run services describe polls-service --platform managed \
    --region northamerica-northeast1 --format "value(status.url)") -->

SERVICE_URL=$(gcloud run services describe hello-world --platform managed \
    --region northamerica-northeast1 --format "value(status.url)")

<!-- gcloud run services update polls-service \
    --platform managed \
    --region northamerica-northeast1 \
    --set-env-vars CLOUDRUN_SERVICE_URL=$SERVICE_URL -->

gcloud run services update hello-world \
    --platform managed \
    --region northamerica-northeast1 \
    --set-env-vars CLOUDRUN_SERVICE_URL=$SERVICE_URL

# sign in to /admin :get password: 
 gcloud secrets versions access latest --secret superuser_password && echo ""


# to run - add deploy step to yaml and 
gcloud builds submit --config cloudbuild.yaml or add trigger
```
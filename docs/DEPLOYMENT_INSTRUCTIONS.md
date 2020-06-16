## Deploying the Application

### Setup
Requirements:
 - Google Platform (GCP) account
 - Google SDK
 - Docker
 - GitHub account
 - CircleCI account

Setup Project with SDK:
 - Run 'gcloud init' to access GCP using your account credentials
 - Run 'gcloud projects create `[PROJECT_ID]` --enable-cloud-apis --folder `[FOLDER_ID]` --name=`[NAME]`'
 - Run 'gcloud config set project `[PROJECT_ID]`'

Enable APIs:
 - Run 'gcloud services list --available'
 - Run 'gcloud services enable `bigquery.googleapis.com` `bigquerydatatransfer.googleapis.com` `cloudscheduler.googleapis.com` `container.googleapis.com` `containerregistry.googleapis.com` `monitoring.googleapis.com` `storage-component.googleapis.com` `run.googleapis.com`' 

Create and Download Service Account Key:
 - Run 'gcloud iam service-accounts keys create ~/key.json \
  --iam-account `[SERVICE_ACCOUNT_NAME]`@project-id.iam.gserviceaccount.com'
 - Copy file to app/api folder
 - Edit run_api.sh file and replace `healthcare-predictions-85c2b5783a5e.json` to your JSON key file name

Set Credentials:
 - Run 'export GOOGLE_APPLICATION_CREDENTIALS=`[PATH]`/`[FILENAME].json`'
 
Setup Virtual Environment, Test, and Install Dependencies:
 - Run 'make all'
 
### ETL
Push Scraper Application to Google Container Registry (GCR):
 - Go to 'cms-scrape' folder
 - Run 'gcloud auth configure-docker'
 - Run 'docker build --tag=`[IMAGE_NAME]:[VERSION]` .'
 - Run 'docker tag `[IMAGE_NAME]:[VERSION]` `gcr.io/[PROJECT_ID]/[IMAGE_NAME]:[VERSION]`'
 - Run 'docker push `gcr.io/[PROJECT_ID]/[IMAGE_NAME]:[VERSION]`'

Deploy to Cloud Run:
 - Run gcloud 'run deploy --image `gcr.io/[PROJECT_ID]/[IMAGE_NAME]:[VERSION]` --platform managed'
 - Enter service name
 - Select region (i.e us-central1)
 - Enter `n` for `allow unauthenticated invocations`
 - Copy service URL

Setup Cloud Scheduler:
 - Run ' gcloud scheduler jobs create http `${JOB_ID}` --schedule=`"every monday 09:00"` --uri=`${URI}` --oidc-service-account-email=`${[SERVICE_ACCOUNT_NAME]@project-id.iam.gserviceaccount.com}`' (Note: schedule can be any Crontab compatible string)
 - Go to Cloud Scheduler from Cloud Console and click 'RUN NOW' (https://console.cloud.google.com/cloudscheduler)
 
Check to see if files are in Cloud Storage:
- Run 'gsutil ls'
- There should be two buckets: `gs://cms-beneficiary/` and `gs://cms-inpatient/`
 
Setup BigQuery Dataset:
 - Run 'bq ls `[PROJECT_ID]`:' will initialize BigQuery API and list datasets
 - Choose project
 - Run 'bq mk `[DATASET]`'
 
Create and Load Data to Tables:
 - Run 'bq load --source_format=PARQUET `[DATASET].[TABLE_NAME]` `gs://cms-beneficiary/*.parquet`'
 - Run 'bq load --source_format=PARQUET `[DATASET].[TABLE_NAME]` `gs://cms-inpatient/*.parquet`'

Setup Big Query Recurring Transfer:
 - Follow guidelines here: https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer

### BigQuery ML
Extract Features and Load Data to New Table:
 - Run 'bq query --destination_table `[PROJECT_ID]:[DATASET].[FEATURES_TABLE_NAME]` --use_legacy_sql=false "SELECT DISTINCT inpatient_claims.DESYNPUF_ID AS PATIENT_ID, CLM_ID, BENRES_IP AS ANNUAL_COST, DATE_DIFF(CASE WHEN CLM_FROM_DT IS NULL THEN '2008-01-01' ELSE CLM_FROM_DT END, BENE_BIRTH_DT, YEAR) AS AGE, BENE_SEX_IDENT_CD AS GENDER, BENE_RACE_CD AS RACE, SP_STATE_CODE AS STATE, SP_ALZHDMTA AS ALZHEIMERS, SP_CHF AS HEART_FAILURE, SP_CHRNKIDN AS KIDNEY_DISEASE, SP_CNCR AS CANCER, SP_COPD AS COPD, SP_DEPRESSN AS DEPRESSION, SP_DIABETES AS DIABETES, SP_ISCHMCHT AS HEART_DISEASE, SP_OSTEOPRS AS OSTEOPOROSIS, SP_RA_OA AS ARTHRITIS, SP_STRKETIA AS STROKE, COUNT(CASE WHEN ICD9_DGNS_CD_1 = 'nan' THEN NULL ELSE 1 END) AS DX, COUNT(CASE WHEN ICD9_PRCDR_CD_1 = 'nan' THEN NULL ELSE 1 END) AS PX, COUNT(CASE WHEN HCPCS_CD_1 = 'nan' THEN NULL ELSE 1 END) AS HCPCS FROM cms.inpatient_claims INNER JOIN cms.beneficiary_summary ON inpatient_claims.DESYNPUF_ID = beneficiary_summary.DESYNPUF_ID WHERE BENRES_IP > 0 GROUP BY inpatient_claims.DESYNPUF_ID, CLM_ID, BENRES_IP, BENE_BIRTH_DT, CLM_FROM_DT, BENE_SEX_IDENT_CD, BENE_RACE_CD, SP_STATE_CODE, SP_ALZHDMTA, SP_CHF, SP_CHRNKIDN, SP_CNCR, SP_COPD, SP_DEPRESSN, SP_DIABETES, SP_ISCHMCHT, SP_OSTEOPRS, SP_RA_OA, SP_STRKETIA"'

Create ML Model:
 - Run 'bq query --use_legacy_sql=false "CREATE OR REPLACE MODEL `[DATASET].[MODEL_NAME]` TRANSFORM(ANNUAL_COST, ML.QUANTILE_BUCKETIZE(AGE, 5) OVER() AS BUCKETIZED_AGE, CAST(GENDER AS STRING) AS GENDER, CAST(RACE AS STRING) AS RACE, CAST(STATE AS STRING) AS STATE, CAST(ALZHEIMERS AS STRING) AS ALZHEIMERS, CAST(HEART_FAILURE AS STRING) AS HEART_FAILURE, CAST(KIDNEY_DISEASE AS STRING) AS KIDNEY_DISEASE, CAST(CANCER AS STRING) AS CANCER, CAST(COPD AS STRING) AS COPD, CAST(DEPRESSION AS STRING) AS DEPRESSION, CAST(DIABETES AS STRING) AS DIABETES, CAST(HEART_DISEASE AS STRING) AS HEART_DISEASE, CAST(OSTEOPOROSIS AS STRING) AS OSTEOPOROSIS, CAST(ARTHRITIS AS STRING) AS ARTHRITIS, CAST(STROKE AS STRING) AS STROKE, DX, PX, HCPCS)  OPTIONS (MODEL_TYPE='LINEAR_REG', INPUT_LABEL_COLS=['ANNUAL_COST'], OPTIMIZE_STRATEGY='BATCH_GRADIENT_DESCENT', L2_REG=1, MAX_ITERATIONS=50, LEARN_RATE_STRATEGY='LINE_SEARCH', LS_INIT_LEARN_RATE=.01, EARLY_STOP=TRUE, DATA_SPLIT_METHOD='RANDOM', DATA_SPLIT_EVAL_FRACTION=.10) AS SELECT * FROM `[DATASET].[FEATURES_TABLE_NAME]`"'

Create Requests Table:
 - Run 'bq query  --use_legacy_sql=false CREATE TABLE `[DATASET].[REQUESTS_TABLE_NAME]` (ID STRING, AGE INT64, GENDER INT64, RACE INT64, STATE INT64, ALZHEIMERS INT64, HEART_FAILURE INT64, KIDNEY_DISEASE INT64, CANCER INT64, COPD INT64, DEPRESSION INT64, DIABETES INT64, HEART_DISEASE INT64, OSTEOPOROSIS INT64, ARTHRITIS INT64, STROKE INT64, DX INT64, PX INT64, HCPCS INT64)' 

### Setting up Kubernetes Cluster on Google Kubernetes Engine (GKE)
Install Kubernetes CLI:
 - Run 'gcloud components install kubectl'
 - Enter `y`
 
Create Cluster:
 - Run 'gcloud container clusters create `[CLUSTER_NAME]` \
 --zone `[COMPUTE_ZONE]` \
 --machine-type=`[MACHINE_TYPE]` \
 --num-nodes=`[NUM_NODES]` \
 --enable-stackdriver-kubernetes \
 --scopes=bigquery,storage-rw'

Get Authentication Credentials for Cluster
 - Run 'gcloud container clusters get-credentials `[CLUSTER_NAME]`'

Create Namespace
 - Run 'kubectl create namespace `[NAME]`'

### Build Application Images, Push to Container Registry, and Deploy to Kubernetes Cluster
#### API
Build and Push API Image to GCR
 - Go to app/api/lib folder
 - Edit insert.py and change `database` to `[PROJECT_ID]` and `cms.prediction_requests` to `[DATASET].[REQUESTS_TABLE_NAME]`
 - Edit prediction.py and chage `database` to `[PROJECT_ID]`, `cms.model_v1` to `[DATASET].[MODEL_NAME]`, and `cms.prediction_requests` to `[DATASET].[REQUESTS_TABLE_NAME]`
 - Go to app/api 
 - Run 'docker build --tag=`[IMAGE_NAME]:[VERSION]`
 - Run 'docker tag `[IMAGE_NAME]:[VERSION]` `gcr.io/[PROJECT_ID]/[IMAGE_NAME]:[VERSION]`
 - Run 'docker push `gcr.io/[PROJECT_ID]/[IMAGE_NAME]:[VERSION]`
 
Deploy the API
 - Open api-deployment.yaml file in app/k8s/deployments/
 - Under `containers` change `name` to `[IMAGE_NAME]` and `image` to `gcr.io/[PROJECT_ID]/[IMAGE_NAME]:[VERSION]` for API
 - Save file
 - Run 'kubectl apply --namespace `[NAME]` -f app/k8s/deployments/api-deployment.yaml'
 - Run 'kubectl apply --namespace `[NAME]` -f app/k8s/services/api-service.yaml'

Setup Horizontal Pod Autoscaling
  - Run 'kubectl apply --namespace `[NAME]` -f app/k8s/pods/api-hpa.yaml'

Create Firewall Rules to Allow TCP Traffic to API Node Port
 - Run 'kubectl get service api-service --output yaml --namespace `[NAME]`' to get node port value for API
 - Run 'kubectl get nodes --output wide' to get external IP address for the node(s)
 - Run 'gcloud compute firewall-rules create `[NODE_PORT_NAME]` --allow tcp:`[NODE_PORT_VALUE]`'
 
#### Front-end
Build and Push Front-end Image to GCR
 - Go to app/frontend folder
 - Edit app.py and change URL paths to `[NODE_IP_ADDRESS]:[NODE_PORT_VALUE]` for API 
 - Run 'docker build --tag=`[IMAGE_NAME]:[VERSION]`
 - Run 'docker tag `[IMAGE_NAME]:[VERSION]` `gcr.io/[PROJECT_ID]/[IMAGE_NAME]:[VERSION]`
 - Run 'docker push `gcr.io/[PROJECT_ID]/[IMAGE_NAME]:[VERSION]`

Deploy the Front-end
 - Open frontend-deployment.yaml file in app/k8s/deployments/
 - Under `containers` change `name` to `[IMAGE_NAME]` and `image` to `gcr.io/[PROJECT_ID]/[IMAGE_NAME]:[VERSION]` for front-end
 - Save file
 - Run 'kubectl apply --namespace `[NAME]` -f app/k8s/deployments/frontend-deployment.yaml'
 - Run 'kubectl apply --namespace `[NAME]` -f app/k8s/services/frontend-service.yaml'
 
Create Firewall Rules to Allow TCP Traffic to Node Ports
 - Run 'kubectl get service frontend-service --output yaml --namespace `[NAME]`' to get node port value for front-end
 - Run 'kubectl get nodes --output wide' to get external IP address for the node(s)
 - Run 'gcloud compute firewall-rules create `[NODE_PORT_NAME]` --allow tcp:`[NODE_PORT_VALUE]`' for front-end
 
#### Ingress
Setup Ingress Controller with GKE Ingress:
  - Run 'kubectl apply --namespace `[NAME]` -f app/k8s/services/ingress.yaml'
  - Go to https://console.cloud.google.com/networking/addresses/ and change load balancer service 'Type' to 'Static' for static IP address.
 
### CI/CD with CircleCI
Setup Environment Variables:
 - `GOOGLE_PROJECT_ID` 
   - Set project ID
 - `GOOGLE_COMPUTE_ZONE`
   - Set compute zone for Kubernetes cluster 
 - `GCLOUD_SERVICE_KEY`
   - Copy entire contents of JSON key file

Change Configuration File:
 - Change `working_directory` to your directory
 - Build and Push Docker Images
   - Under `Build-Push-Image-Docker-API` change `~/cms-kubernetes/app/api/healthcare-predictions-85c2b5783a5e.json` to `~/[YOUR_WORKING DIRECTORY]/app/api/[JSON_KEY_FILENAME]`
   - Under `gcr/build-image` make these changes:
     - image: `[IMAGE_NAME]`
     - path: `[PATH_TO_DOCKERFILE]`
     - tag: `[VERSION]`
 - deploy
   - Change `cluster` to `[CLUSTER_NAME]`
   - Change `container` to `[IMAGE_NAME]`
   - Change `image` to `gcr.io/[PROJECT_ID]/[IMAGE_NAME]`
   - Change `namespace` to `[NAME]`
   - Change `tag` to `[VERSION]`
 - load-test
   - Change `host` to `[YOUR_HOST]`

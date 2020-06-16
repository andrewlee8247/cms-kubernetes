# Kubernetes Project Using GKE - Medicare Cost Predictions
[![CircleCI](https://circleci.com/gh/andrewlee8247/cms-kubernetes.svg?style=svg)](https://circleci.com/gh/andrewlee8247/cms-kubernetes)

This is a Kubernetes project that deploys an application through a microservices structure using a Docker container registry. Deployment, scaling, and operations are automated through a CI/CD pipeline. Application is deployed to a managed Kubernetes cluster on Google's Kubernetes Engine (GKE). The project's goal was to build a minimum viable product (MVP) for an application that provides predictions on annual healthcare responsibility costs for patients on Medicare based on their chronic medical condition(s). The MVP can be expanded to build a fully featured application to help patients, healthcare providers, and insurers outside of Medicare estimate annual costs.

Main components of this repo include:
 - Application files for API and front-end service
 - Kubernetes deployment and service manifests
 - Manifests for horizontal pod autoscaling and ingress controller
 - Application files for web scraping application
 - Docker files to build image containers
 - Test files and configuration for application services
 - Load test configuration for Locust load testing tool
 - Configuration file for CI/CD pipeline using CircleCI

YouTube demo on application development and deployment found here: https://www.youtube.com/watch?v=edEfjxm5jKk

## About the Data
Data for the project was collected from the Centers for Medicare and Medicaid Services (CMS). The data included beneficiary summaries, demographic factors, chronic medical conditions, annual costs, and inpatient claims from 2008 to 2010. Files are available through their website: https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF

Datasets used contained 8,093,342 observations with 112 explanatory variables and 1 response variable. Median annual healthcare cost for patients with chronic medical conditions was $1,068.00, with a maximum of $53,096, and minimum of $1,024.00. Mean cost was $1,585.48. 57% of the patients were female and 43% were male.

The following graph shows total annual cost by chronic condition:

![Annual-Cost](https://i.ibb.co/LNSg2zW/benresip-1.png)
  
## How it works
On top of Google's Kubernetes Engine (GKE), the system utilizes different services and APIs on the Google Cloud Platform (GCP) to run the application. Python was used as the primary language to build the application. A Flask application running on Cloud Run was built to automatically extract, transfrom, and load (ETL) data to Cloud Storage and BigQuery (data warehouse). For the predictions, a linear regression model was built using BigQuery ML based on patient’s age, gender, race, state, medical condition(s), number of diagnosis claims, procedures, and services outside of primary insurance. Patient’s annual cost was used as the target/response variable. BigQuery ML is a tool that enables users to create and execute machine learning models in BigQuery by using SQL queries.  

The front-end was built using Flask and Dash utilizing Bootstrap components to support the user interface. The REST API was also built using Flask, and the documentation was generated using Swagger. The API's resources can be visualized and interaction can take place with the Swagger UI. Both front-end and API services were containerized using Docker and pushed to Google's Container Registry (GCR). The containers were then deployed to a cluster running on GKE. Continuous integration and continuous deployment are in place utilizing CircleCI. Code edited locally and pushed to GitHub will initialize the CI/CD workflow, which will automatically test, build and push the application container images to Google's Container Registry (GCR), and the services will be deployed to the Kubernetes cluster. A load test is run afterwards to ensure application functionality.

The REST API takes a JSON payload that inserts parameter data into BigQuery and makes a prediction request to the model built using BigQuery ML, which then returns the prediction as a JSON response. The front-end UI provides a form for a user to fill out such as age, gender, race, medical condition(s), and so on. When a user clicks submit, a request is made to the API and the JSON response is rendered as an HTML output.

<p align="center">
   <img width="720" height="408" src="https://i.ibb.co/XS9qkwM/gke.gif">
</p>

## System Architecture
![System-Architecture](https://i.ibb.co/4FPfM7p/CMS-System-Architecture.png)
1. Using Cloud Scheduler, a weekly batch process is run using an application built in Flask that was deployed to Cloud Run. The application scrapes all files from the CMS website, converts them into Parquet files, and loads them to Cloud Storage. Data from files are loaded to BigQuery using the BigQuery Transfer Service. Stackdriver monitoring was setup to monitor the entire system. 
2. CI/CD was set up using CircleCI and updates to the application are tested, containerized, and images are automatically pushed to the Google Container Registry and deployed to the Kubernetes cluster.
3. Kubernetes cluster has two services: one for the API and one for the front-end. Services were exposed to node ports. Firewall rules were also created to allow TCP traffic to node ports. Horizontal pod autoscaling was set up to ensure services do not go down in case of pod failure. The API sends prediction requests to BigQuery through the BigQuery API and predictions are made using a model built with BigQuery ML.
4. Ingress controller was set up using GKE Ingress for load balancing and routing to the two services.
5. Users/Clients can access the front-end and make requests to the API through the public IP address that was generated by the ingress controller.

Note: Node ports would not be used in production. Path based and subdomain based routing would be used with the ingress controller.

## Getting Started

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
 - Run 'gcloud config set project `[PROJECT_ID]`

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
 --scopes=bigquery, storage-rw'

Get Authentication Credentials for Cluster
 - Run 'gcloud container clusters get-credentials `[CLUSTER_NAME]`'

Create Namespace
 - Run 'kubectl create namespace `[NAME]`'

### CI/CD with CircleCI
Setup Environment Variables:
 - `GOOGLE_PROJECT_ID` 
   - Set project ID
 - `GOOGLE_COMPUTE_ZONE`
   - Set compute zone for Kubernetes cluster 
 - `GCLOUD_SERVICE_KEY`
   - Copy entire contents of JSON key file
 
 GCP Integration Packages:
  - Google Kubernetes Engine (GKE): `circleci/gcp-gke@1.0.4`
  - Google Container Registry (GCR): `circleci/gcp-gcr@0.7.1`
  - Google Cloud CLI: `circleci/gcp-cli@1.8.4`

#### For detailed instructions on deploying the entire application from this repository click <a href="https://github.com/andrewlee8247/cms-kubernetes/blob/master/docs/DEPLOYMENT_INSTRUCTIONS.md">here</a>.

## Resources:
 - https://cloud.google.com/bigquery-ml/docs
 - https://cloud.google.com/kubernetes-engine/docs
 - https://kubernetes.io
 - https://circleci.com/orbs/registry/?query=gcp

## Future plans:
 - Build better security for API by adding token based authentication.
 - Implement Infrastructure as Code (IaC) service for better configuration and automation.
 - Build and test other models for better accuracy/lower RMSE scores. 
 - Setup vertical pod autoscaling and cluster autoscaling with node auto-provisioning.
 - Setup service mesh for better load balancing, failure recovery, and lower latency.

# Getting started with Prefect Cloud & Google Cloud

This repository includes example project structure with your first flows and custom blocks. 

GitHub Action deploying Prefect agent as a container to a VM hosted in the Google Compute Engine.


## Prerequisites

### Prefect Cloud

Sign up for a [Prefect Cloud](https://app.prefect.cloud/) account.

Make sure to create a workspace and create an API key.
Then, add both ``PREFECT_API_KEY`` and ``PREFECT_API_URL``as GitHub Actions secrets.


### Google Cloud

Create a GCP project and a service account. Here's how you can create all that from ``gcloud`` CLI, e.g. using Cloud Shell terminal:

```bash
# Create GCP account + project => here we use project named "prefect-community" - replace it with your project name
# This will also set default project and region:
export CLOUDSDK_CORE_PROJECT="prefect-community"
export CLOUDSDK_COMPUTE_REGION=us-east1
export GCP_AR_REPO=prefect
export GCP_SA_NAME=prefect

# enable required GCP services:
gcloud services enable iamcredentials.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable compute.googleapis.com

# create service account named e.g. prefect:
gcloud iam service-accounts create $GCP_SA_NAME
export MEMBER=serviceAccount:"$GCP_SA_NAME"@"$CLOUDSDK_CORE_PROJECT".iam.gserviceaccount.com
gcloud projects add-iam-policy-binding $CLOUDSDK_CORE_PROJECT --member=$MEMBER --role="roles/run.admin"
gcloud projects add-iam-policy-binding $CLOUDSDK_CORE_PROJECT --member=$MEMBER --role="roles/compute.instanceAdmin.v1"
gcloud projects add-iam-policy-binding $CLOUDSDK_CORE_PROJECT --member=$MEMBER --role="roles/artifactregistry.admin"
gcloud projects add-iam-policy-binding $CLOUDSDK_CORE_PROJECT --member=$MEMBER --role="roles/iam.serviceAccountUser"

# create JSON credentials file as follows, then copy-paste its content into your GHA Secret + Prefect GcpCredentials block:
gcloud iam service-accounts keys create prefect.json --iam-account="$GCP_SA_NAME"@"$CLOUDSDK_CORE_PROJECT".iam.gserviceaccount.com
```
This will generate the JSON key file, of which contents you can copy and paste into your ``GCP_CREDENTIALS`` secret.

# What does the action do?

1. It creates an Artifact Registry repository if one doesn't exist yet. If you don't want this behavior of automatically creating the repository for you if one doesn't exist yet, you can minimize the permissions on your service account from admin to writer: ``"roles/artifactregistry.writer"``
2. It builds a Docker image and pushes it to that Artifact Registry repository, based on ``Dockerfile.agent`` file existing in your custom repository from which you are using this GitHub Action.
3. It deploys a VM (if one such VM with the same name already exists, it gets deleted before a new VM gets created) and a Docker container running the agent process.


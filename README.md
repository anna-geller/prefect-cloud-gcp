# Getting started with Prefect Cloud & Google Cloud

This repository includes example project structure with:
- your first flows and blocks
- all-in-one GitHub Action deploying a custom image and container to a VM hosted in the Google Compute Engine - you can easily modify details such as region, instance type or names for all components
- modular GitHub Actions in case you only want to use this template to deploy a VM, or to only build and push a Docker image to the Google Artifact Registry - the custom modules give you the freedom to choose which component you want to use, and you can deploy those one by one to set up everything more incrementally, and have more control over how you do it.  


[Blog post: GCP and Prefect Cloud — from Docker Container to Cloud VM on Google Compute Engine](https://medium.com/the-prefect-blog/gcp-and-prefect-cloud-from-docker-container-to-cloud-vm-on-google-compute-engine-2dffa026d16b)


## Prerequisites

### Prefect Cloud

Sign up for a [Prefect Cloud](https://app.prefect.cloud/) account.

1. Create a workspace and an API key.
2. Add both ``PREFECT_API_KEY`` and ``PREFECT_API_URL``as GitHub Actions secrets.


### Google Cloud

Create a GCP project and a service account. Here's how you can create all that from ``gcloud`` CLI, e.g. using Cloud Shell terminal (_feel free to customize any names based on your needs_):

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

This will generate the JSON key file, of which contents you can copy and paste into your ``GCP_CREDENTIALS`` secret in:

1. GitHub Action secret named ``GCP_CREDENTIALS``
2. Prefect ``GcpCredentials`` block named ``default``- if you save this Prefect block with a different name, make sure to adjust it in your GitHub Action inputs, e.g. in [`.github/workflows/getting-started.yml`](.github/workflows/getting-started.yml):

```yaml
  gcp_creds_block_name:
    description: 'Name of the GcpCredentials block'
    required: false
    default: "default"
    type: string
```


# What does the main Getting Started action do?

1. It creates an Artifact Registry repository if one doesn't exist yet. That's why the permissions on your service account must be set to admin ``"roles/artifactregistry.admin"`` rather than just a writer: ``"roles/artifactregistry.writer"`` - if you prefer to manually create the repository and limit the service account permissions, you can do that.
2. It builds a Docker image and pushes it to that Artifact Registry repository, based on the [``Dockerfile``](Dockerfile)
3. It deploys a VM (if one such VM with the same name already exists, it gets deleted before a new VM gets created) and a Docker container running a Prefect worker process that deploys flow runs. By default, the flows are configured to be deployed as serverless containers using Google Cloud Run jobs. This makes it easy to scale your project as your needs grow - no need to monitor and maintain the underlying infrastructure - serverless containers gets spun up based on the provided Artifact Registry image and the resource allocation can be adjusted any time on the ``CloudRunJob`` block, even from the Prefect UI.
4. It automatically deploys your first [Prefect blocks](.github/actions/blocks-quickstart/blocks.py)
5. It automatically deploys your first [Prefect flows](flows)



# How does this automated GitHub Actions process deploy flows?

## ``deploy-flows`` action

This action assumes that the name of your `flow_script.py` matches the name of the flow, e.g. the flow script ``parametrized.py`` has a function named ``parametrized()`` decorated with `@flow`. This means that if your script `parametrized.py` has multiple flows within, only the flow `parametrized` gets deployed (and potentially scheduled) as part of your Prefect Cloud deployment:


```python
from prefect import get_run_logger, flow
from typing import Any


@flow(log_prints=True)
def some_subflow():
    print("I'm a subflow")

    
@flow
def parametrized(
    user: str = "Marvin", question: str = "Ultimate", answer: Any = 42
) -> None:
    logger = get_run_logger()
    logger.info("Hello from Prefect, %s! 👋", user)
    logger.info("The answer to the %s question is %s! 🤖", question, answer)


if __name__ == "__main__":
    parametrized(user="World")
```

You can still create a deployment for the flow ``some_subflow`` if you want to, but the default GitHub Action here won't do it for you - this is not a Prefect limitation, it's only a choice made in this demo to make the example project here easier to follow (and more standardized to deploy in an automated CI/CD pipeline).

> As an alternative approach to naming the main flow the same way as the script name, you could consider naming each main flow that needs to get schedule as ``main``.


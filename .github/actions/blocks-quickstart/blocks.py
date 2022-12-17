"""
python blocks.py -b $GITHUB_REF_NAME -r "$GITHUB_SERVER_URL/$GITHUB_REPOSITORY" \
-n ${{ inputs.block_name }} -i ${{ inputs.image_uri }} --region ${{ inputs.region }}
"""
import argparse
from prefect.filesystems import GitHub
from prefect_gcp.cloud_run import CloudRunJob
from prefect_gcp.credentials import GcpCredentials

REPO = "https://github.com/anna-geller/prefect-cloud-gcp"
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--branch", default="main")
parser.add_argument("-r", "--repo", default=REPO)

parser.add_argument("-n", "--block-name", default="default")
parser.add_argument("-i", "--image")
parser.add_argument("--region", default="us-east1")

args = parser.parse_args()

gh = GitHub(repository=args.repo, reference=args.branch)
gh.save(args.block_name, overwrite=True)

block = CloudRunJob(
    image=args.image,
    region=args.region,
    credentials=GcpCredentials.load(args.block_name),
    cpu=1,
    timeout=3600,
)
block.save(args.block_name, overwrite=True)

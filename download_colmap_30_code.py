import os
from pathlib import Path

import oss2


OSS_AK = os.environ.get("OSS_AK", "")
OSS_SK = os.environ.get("OSS_SK", "")
OSS_ENDPOINT = os.environ.get("OSS_ENDPOINT", "")
OSS_BUCKET = os.environ.get("OSS_BUCKET", "")

OSS_PREFIX = os.environ.get("CODE_REPO_PREFIX", "output/code_repo").strip("/")
WORKSPACE_DIR = Path(os.environ.get("WORKSPACE_DIR", "/workspace"))
PIPELINE_DIR = Path(os.environ.get("PIPELINE_DIR", str(WORKSPACE_DIR / "colmap_pipeline")))


def download_file(bucket, oss_key: str, local_path: Path):
    local_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {oss_key} -> {local_path}")
    bucket.get_object_to_file(oss_key, str(local_path))


def main():
    auth = oss2.Auth(OSS_AK, OSS_SK)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET)

    worker_oss_key = f"{OSS_PREFIX}/worker_colmap_30.py"
    pipeline_oss_key = f"{OSS_PREFIX}/run_pipeline_incremental_v6.py"

    worker_local_path = WORKSPACE_DIR / "worker_colmap_30.py"
    pipeline_local_path = PIPELINE_DIR / "run_pipeline_incremental_v6.py"

    download_file(bucket, worker_oss_key, worker_local_path)
    download_file(bucket, pipeline_oss_key, pipeline_local_path)

    print("Done.")
    print(f"  worker  : {worker_local_path}")
    print(f"  pipeline: {pipeline_local_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Скрипт для запуску ноутбука на Vertex AI
"""

from google.cloud import aiplatform

def run_notebook_on_vertex(
    project_id: str,
    location: str,
    bucket_name: str,
    notebook_path: str = "homework_5.ipynb"
):
    """Запускає ноутбук на Vertex AI"""
    
    aiplatform.init(project=project_id, location=location)
    
    job = aiplatform.CustomContainerTrainingJob(
        display_name="seq2seq-training",
        container_uri="gcr.io/deeplearning-platform-release/pytorch-gpu.1-13",
    )
    
    job.run(
        replica_count=1,
        machine_type="n1-standard-4",
        accelerator_type="NVIDIA_TESLA_T4",
        accelerator_count=1,
        base_output_dir=f"gs://{bucket_name}/output",
        args=[
            "--notebook-path", notebook_path,
        ],
    )
    
    print(f"✅ Job submitted: {job.resource_name}")

if __name__ == "__main__":
    run_notebook_on_vertex(
        project_id="project-7e1433c8-b894-49bd-ad4",
        location="us-central1",
        bucket_name="your-ml-experiments"
    )

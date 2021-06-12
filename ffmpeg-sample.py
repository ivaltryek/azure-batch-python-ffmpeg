# This function flips the video vertically.

import ffmpeg
import subprocess
import sys

import azure.storage.blob as azureblob
import azure.batch._batch_service_client as batch
import azure.batch.batch_auth as batchauth
import azure.batch.models as batchmodels

task_commands = [
    'python3 ffmpeg-sample.py'
]

task_resource_files_urls = [
    
]

def create_job(batch_service_client, job_id, pool_id):
    """
   Creates a job with the specified ID, associated with the specified pool.
   :param batch_service_client: A Batch service client.
   :type batch_service_client: `azure.batch.BatchServiceClient`
   :param str job_id: The ID for the job.
   :param str pool_id: The ID for the pool.
   """

    print(f'Creating Job [{job_id}]...')
    job = batch.models.JobAddParameter(
        id=job_id,
        pool_info=batch.models.PoolInformation(pool_id=pool_id))

    batch_service_client.job.add(job)
    

def flip():
    stream = ffmpeg.input('countdown.mov')
    stream = ffmpeg.vflip(stream)
    stream = ffmpeg.output(stream, 'output.mp4')
    ffmpeg.run(stream)


flip()

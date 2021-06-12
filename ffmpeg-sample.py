# This file calls the Azure batch API and starts the job.


from config import _STORAGE_ACCOUNT_NAME,_STORAGE_ACCOUNT_KEY,_BATCH_ACCOUNT_NAME, _BATCH_ACCOUNT_KEY, _BATCH_ACCOUNT_URL, _POOL_ID, _POOL_VM_SIZE, _POOL_NODE_COUNT 
import os
import datetime
import time
import io
import sys
import azure.storage.blob as azureblob
import azure.batch._batch_service_client as batch
import azure.batch.batch_auth as batchauth
import azure.batch.models as batchmodels




def create_job(batch_service_client, job_id, pool_id):
    """
    Creates a job with the specified ID, associated with the specified pool.
    :param batch_service_client: A Batch service client.
    :type batch_service_client: `azure.batch.BatchServiceClient`
    :param str job_id: The ID for the job.
    :param str pool_id: The ID for the pool.
    """
    print('Creating job [{}]...'.format(job_id))

    job = batch.models.JobAddParameter(
        id=job_id,
        pool_info=batch.models.PoolInformation(pool_id=pool_id))

    batch_service_client.job.add(job)


def wait_for_tasks_to_complete(batch_service_client, job_id, timeout):
    """
    Returns when all tasks in the specified job reach the Completed state.
    :param batch_service_client: A Batch service client.
    :type batch_service_client: `azure.batch.BatchServiceClient`
    :param str job_id: The id of the job whose tasks should be to monitored.
    :param timedelta timeout: The duration to wait for task completion. If all
    tasks in the specified job do not reach Completed state within this time
    period, an exception will be raised.
    """
    timeout_expiration = datetime.datetime.now() + timeout

    print("Monitoring all tasks for 'Completed' state, timeout in {}..."
          .format(timeout), end='')

    while datetime.datetime.now() < timeout_expiration:
        print('.', end='')
        sys.stdout.flush()
        tasks = batch_service_client.task.list(job_id)

        incomplete_tasks = [task for task in tasks if
                            task.state != batchmodels.TaskState.completed]
        if not incomplete_tasks:
            print()
            return True
        else:
            time.sleep(1)

    print()
    raise RuntimeError("ERROR: Tasks did not reach 'Completed' state within "
                       "timeout period of " + str(timeout))


def _read_stream_as_string(stream, encoding):
    """Read stream as string
    :param stream: input stream generator
    :param str encoding: The encoding of the file. The default is utf-8.
    :return: The file content.
    :rtype: str
    """
    output = io.BytesIO()
    try:
        for data in stream:
            output.write(data)
        if encoding is None:
            encoding = 'utf-8'
        return output.getvalue().decode(encoding)
    finally:
        output.close()
    raise RuntimeError('could not write data to stream or decode bytes')


def print_task_output(batch_service_client, job_id, encoding=None):
    """Prints the stdout.txt file for each task in the job.
    :param batch_client: The batch client to use.
    :type batch_client: `batchserviceclient.BatchServiceClient`
    :param str job_id: The id of the job with task output files to print.
    """

    print('Printing task output...')

    tasks = batch_service_client.task.list(job_id)

    for task in tasks:

        node_id = batch_service_client.task.get(
            job_id, task.id).node_info.node_id
        print("Task: {}".format(task.id))
        print("Node: {}".format(node_id))

        stream = batch_service_client.file.get_from_task(
            job_id, task.id, 'stdout.txt')

        file_text = _read_stream_as_string(
            stream,
            encoding)
        print("Standard output:")
        print(file_text)

task_resource_files_urls = [
    'https://raw.githubusercontent.com/meet86/azure-batch-python-ffmpeg/main/task.py'
]

command = "/bin/bash -c \"python3 task.py testparam\""

task_resource_files = [batchmodels.ResourceFile(file_path=os.path.basename(
    file_url), http_url=file_url) for file_url in task_resource_files_urls]


tasks_creation_information = list()

tasks_creation_information.append(batch.models.TaskAddParameter(
    id='Task01',
    command_line=command,
    resource_files=task_resource_files
))



# This file contains environment variables.
credentials = batchauth.SharedKeyCredentials(
    _BATCH_ACCOUNT_NAME, _BATCH_ACCOUNT_KEY)

batch_client = batch.BatchServiceClient(credentials, _BATCH_ACCOUNT_URL)

create_job(batch_client, 'TestJob', _POOL_ID)

batch_client.task.add_collection('TestJob', tasks_creation_information)

wait_for_tasks_to_complete(batch_client,
                           'TestJob',
                           datetime.timedelta(minutes=30))

print("  Success! All tasks reached the 'Completed' state within the "
      "specified timeout period.")

# Print the stdout.txt and stderr.txt files for each task to the console
print_task_output(batch_client, 'TestJob')

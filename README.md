# Azure Batch Using Python and FFmpeg

Hi!, This project demonstrates how to run custom python script with any pip dependencies. In this project, I've simply used the FFmpeg.

I've decied to write proper README, because there are very less resources on this particular example.

# Prerequisites
 Make sure you have properly configured the Azure Batch Account and also ran the startup script when creating the Batch pool.

Below is the example that how to write the startup script

```shell
/bin/bash -c "apt-get update && apt-get install -y python3-pip && python3 -m pip install azure-storage-blob==12.3.1 numpy==1.18.1 && apt-get install -y ffmpeg x264
```
Make sure you append && with every new command, to get proper installation process.

# Setup
Make sure you have latest python version installed or atleast LTS one.
Run this command to install all the dependencies,

    pip install -r requirements.txt

## Working with main file
Main Python logic is stored in file called **task.py**
Here's the snapshot of that file
```python
import ffmpeg
import subprocess
import sys
import logging

logging.basicConfig(level = logging.INFO)

def flip():
	logging.info('Processing Started')
	stream = ffmpeg.input('FileURL with http')
	stream = ffmpeg.vflip(stream)
	stream = ffmpeg.output(stream, 'output.mp4')
	logging.info(sys.argv[1])
	ffmpeg.run(stream)
	logging.info('Finished')

flip()
```
change the File URL which is actually downloadable, if not then code will fail.

To run this file,

    python task.py testparam

## config.py

This file holds all the confidential variables or settings of Azure batch which are used to connect using pip package.

So, Basic config.py will look like this,

```python
_BATCH_ACCOUNT_NAME = ''  # Your batch account name
_BATCH_ACCOUNT_KEY = ''  # Your batch account key
_BATCH_ACCOUNT_URL = ''  # Your batch account URL
_STORAGE_ACCOUNT_NAME = ''  # Your storage account name
_STORAGE_ACCOUNT_KEY = ''  # Your storage account key
_POOL_ID = 'PythonQuickstartPool'  # Your Pool ID
_POOL_NODE_COUNT = 2  # Pool node count
_POOL_VM_SIZE = 'STANDARD_A1_v2'  # VM Type/Size
_JOB_ID = 'PythonQuickstartJob'  # Job ID
_STANDARD_OUT_FILE_NAME = 'stdout.txt'  # Standard Output fil
```

## 

## Running task with the Azure Batch
**ffmpeg-sample.py** contains the API calls made with the Azure Batch PiP package.

### Walkthrough of the file
Go to :144

```python
task_resource_files_urls = [
    'https://raw.githubusercontent.com/meet86/azure-batch-python-ffmpeg/main/task.py'
]
```

Here, List out all the files that are dependecies or the main program file.
Because, these files will be uploaded to the azure batch job.

```python
command =  "/bin/bash -c \"python3 task.py testparam\""
```
This command will be feeded into the Job method to run the task.

## References
https://github.com/Azure-Samples/batch-python-quickstart/


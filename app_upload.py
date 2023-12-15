from flask import Flask, request, render_template
from azure.storage.blob import BlobServiceClient, generate_container_sas, ContainerSasPermissions
import os
import datetime

app = Flask(__name__)

# Azure Storage Account and SAS Token details
account_name = "storageaniketdp203"
container_name = "master"
sas_token = '?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupyx&se=2023-12-15T14:44:21Z&st=2023-12-14T06:44:21Z&spr=https&sig=tZG1c4QOIoQbaKN0IKmEy8Hg1ET3xk3XrLxRovA8J%2B0%3D'

blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=sas_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', message='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', message='No selected file')

    # Upload the file to Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
    blob_client.upload_blob(file)

    return render_template('index.html', message='File uploaded successfully')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template, redirect, url_for
from azure.storage.blob import BlobServiceClient, generate_container_sas, ContainerSasPermissions
import os
import datetime
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = '1234567890'  # Secret key


# Azure Storage Account and SAS Token details
account_name = "storageaniketdp203"
container_name = "master"
sas_token = '?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupyx&se=2023-12-15T14:44:21Z&st=2023-12-14T06:44:21Z&spr=https&sig=tZG1c4QOIoQbaKN0IKmEy8Hg1ET3xk3XrLxRovA8J%2B0%3D'

blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=sas_token)

@app.route('/')
def index():
    # List the blobs in the "master/images" folder
    blob_prefix = "images/"
    blobs = [blob.name[len(blob_prefix):] for blob in blob_service_client.get_container_client(container_name).list_blobs(name_starts_with=blob_prefix)]
    # Generate URLs for each blob with the SAS token
    blob_urls = [f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_prefix}{blob}{sas_token}" for blob in blobs]

    return render_template('index.html', blob_urls=blob_urls)


@app.route('/upload', methods=['POST' ,'GET'])
def upload():
    # Generate a pandas graph (replace this with your actual graph generation code)
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    ax = df.plot(x='x', y='y')
    fig = ax.get_figure()

    # Convert the plot to bytes
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    # Upload the file to Azure Blob Storage
    blob_name = "\images"
    container_path = container_name+blob_name
    blob_client = blob_service_client.get_blob_client(container=container_path, blob="graph2.png")
    blob_client.upload_blob(buffer.read())

    # Redirect to the index page (or any other page)
    return redirect('/')
  


if __name__ == '__main__':
    app.run(debug=True)
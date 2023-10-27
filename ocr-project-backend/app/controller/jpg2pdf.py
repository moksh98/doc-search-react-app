# Written by:
# Vishva Shah (vpshah@ncsu.edu)
# Revised by:
# Nisarg Shah (nsshah5@ncsu.edu)
# built up on work of Brent Younce and Sahil Mehta under guidance of  Dr. Akram Khater (akhater@ncsu.edu)
# Copyright with Moise A. Khayrallah Center for Lebanese Dispaora Studies - North Carolina State University

import os
import io
import configparser
import boto3
import psycopg2
import re
from PIL import Image
import google
from google.cloud import vision, storage
from google.cloud.vision import ImageAnnotatorClient
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson
import time
from time import strftime,gmtime
from datetime import datetime
import sys
import requests
import pathlib
import pprint

from app.controller.gcv2hocr import *
from app.controller.hocr2pdf import *
from app.controller.sendData import saveFile

from app.core.settings import settings


EXTENSIONS = [".hocr", ".pdf"]

#function to create thumbnail from the uploaded image
def createThumbnail(fullname):
    img = Image.open(os.path.join(settings.FILE_STORE,fullname))

    ##  CREATE THUMBNAILS
    print("...Creating Thumbnail")
    thumb=img.convert("L")
    thumb.thumbnail(size=(256,256))
    
    thumb.save(os.path.join(settings.THUMB_STORE,fullname), optimize=True)

# Google Vision at this point allows images of size < 10 mb for OCR and hence this functions reduces the size of image greater than 10mb.
def reducesize(image,quality):
    if os.stat(os.path.join(settings.FILE_STORE,image)).st_size < 10485760:
        return
    else:
        foo = Image.open(os.path.join(settings.FILE_STORE,image))
        foo.save(os.path.join(settings.FILE_STORE,image),  optimize=True, quality=quality)
        # Scope for improvement 
        if quality-5>0:
            return reducesize(image,quality-5)
    return 


# This function runs Google Vision and extracts text from Image in JSON format, creates HOCR file from this JSON String
def run_google_vision(filename, ext):
    # Checks if the JSON File is already peresnt
    file_name=filename+ext
    HOCR_file=filename+'.hocr'

    if not os.path.isfile(os.path.join(settings.HOCR_STORE,HOCR_file)):
        # Run Google Vision: returns JSON File 
        # TODO configure path
        credentials = service_account.Credentials.from_service_account_file('/home/ubuntu/keyfile/silken-buttress-274819-5ffbc93df39d.json')
        # Instantiates a client
        client = vision.ImageAnnotatorClient(credentials=credentials)
        # Loads the image into memory
        with io.open(os.path.join(settings.FILE_STORE, file_name), 'rb') as image_file:
            content = image_file.read()
        # image = version_v1.types.Image(content=content)
        image=vision.Image(content=content)

        response = client.document_text_detection(image=image)
        # document = response.full_text_annotation
        serialized = MessageToJson(response._pb)
        # texts = response.text_annotations
        string = '{"responses": [\n' + serialized + '\n]}'
        # Google Vision JSON -> HOCR and Saves HOCR file in Temp folder
        GCV2HOCR(string, os.path.join(settings.HOCR_STORE,HOCR_file))
        print("JSON string processed successfully!!!")

def generate_pdf(image_file):
    print(image_file)
    HOCR2PDF(image_file)

# This function backups all the pdfs to S3 bucket.
def savePDF(file, local_path=".", storage_loc=""):
    # AWS_ACCESS = config['pdf_output']['s3_access_key_id']
    AWS_ACCESS = settings.S3_ACCESS_KEY_ID
    # AWS_SECRET = config['pdf_output']['s3_secret_access_key']
    AWS_SECRET = settings.S3_SECRET_ACCESS_KEY
    # AWS_REGION = config['pdf_output']['s3_region_name']
    AWS_REGION = settings.S3_REGION_NAME
    client = boto3.client("s3", aws_access_key_id=AWS_ACCESS, aws_secret_access_key=AWS_SECRET, region_name=AWS_REGION)
    
    # print(str(file))
    client.upload_file(os.path.join(settings.FILE_STORE,file),settings.PDF_S3_BUCKET, file.split("/")[-1] )
    print("...Uploaded on S3")

#This function pushes the file record to the database
async def pushtodb(filename):
    try:
        await saveFile(filename)
    except Exception as e:
        print("Push DB function exception", e)

def indexDoc(filename):
    awsuri="https://"+settings.PDF_S3_BUCKET+".s3.amazonaws.com/"+filename+".pdf"
    response = requests.get("http://"+settings.SOLR_HOSTNAME+"/search-apps/api/index-web?uri="+awsuri)
    print("responce code of REST call for opensemantic:", response.status_code)
    if(response.status_code!=200):
        return False
    print("done opensemn")
    return True

def cleanDirs(filename,extension):
    pdf_file=os.path.join(settings.PDF_STORE,filename+".pdf")
    image_file=os.path.join(settings.FILE_STORE,filename+extension)
    hocr_file=os.path.join(settings.HOCR_STORE,filename+".hocr")
    if(os.path.exists(pdf_file)):
        os.remove(pdf_file)
    if(os.path.exists(hocr_file)):
        os.remove(hocr_file)
    if(os.path.exists(image_file)):
        os.remove(image_file)

def vision_pdf():
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.types.Feature.Type.DOCUMENT_TEXT_DETECTION)
    
    gcs_source = vision.types.GcsSource(uri='/home/ubuntu/inputs/temp.pdf')
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.types.GcsDestination(uri='/home/ubuntu/inputs/output')
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', '/home/ubuntu/inputs/output')
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix, filtering out folders.
    blob_list = [blob for blob in list(bucket.list_blobs(
        prefix=prefix)) if not blob.name.endswith('/')]
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]

    json_string = output.download_as_string()
    response = json.loads(json_string)

    # The actual response for the first page of the input file.
    first_page_response = response['responses'][0]
    annotation = first_page_response['fullTextAnnotation']

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    print('Full text:\n')
    print(annotation['text'])

#--------------------------- MAIN ----------------------------------

# config = configparser.ConfigParser()
# config.read('conf_test.ini')
# if not ('ocr' in config.sections() and 'pdf_output' in config.sections()):
#     print("Invalid configuration")
#     sys.exit(1)

# pdf_out_folder = config['pdf_output']['pdf_out_dir']
# pdf_s3_bucket = config['pdf_output']['pdf_s3_bucket']
# # vision_pdf()
# # subprocess.call('sudo cp -v /home/ubuntu/inputs/*  /home/ubuntu/static/thumbs/',shell=True)

# # images = []
# for ext in ['.jpg', '.jpeg', '.png', '.gif']:
#     images.extend(glob.glob('/home/ubuntu/inputs/*' + ext))

# # for image in images:
# #     f = open("logfile.txt", "a")
# #     f.write("Start: "+strftime("%Y-%m-%d %H:%M:%S", gmtime()))
# #     f.close()
# #     filename, extension = list(os.path.splitext(image))
# #     filename = filename.split('/')[-1]
# #     print("\n\nFile: " + filename + ' ' + extension)
    
# #     reducesize(filename, extension)
# #     print("...Resizing and Backup")
# #     subprocess.call('sudo cp -v /home/ubuntu/inputs/' + filename + extension + ' /home/ubuntu/backup_input/', shell=True)
# #     subprocess.call('sudo mv -v /home/ubuntu/inputs/' + filename + extension + ' /var/www/html/', shell=True)
# #     #subprocess.call('export GOOGLE_APPLICATION_CREDENTIALS="/home/ubuntu/keyfile/silken-buttress-274819-5ffbc93df39d.json"',shell=True)
# #     print("...Running Google Vision")
# #     #print(filename)
# #     run_google_vision(filename, extension)
# #     print("...Generating PDF")
# #     generate_pdf(filename, extension)
    
# #     print("...Moving PDF and Image")
# #     backup([pdf_out_folder + filename + ".pdf"], pdf_s3_bucket)
# #     time.sleep(1.5)
# #     try:
# #         #subprocess.call('opensemanticsearch-index-web https://s3.amazonaws.com/' + pdf_s3_bucket + '/' + filename + ".pdf", shell=True)
# #         urlm = " https://s3.amazonaws.com/"+pdf_s3_bucket+"/"+filename+".pdf"
# #         print(urlm)
# #         subprocess.call('opensemanticsearch-index-web ' +urlm, shell=True, timeout=120)
# #         # subprocess.run(['opensemanticsearch-index-web', urlm], stdout=PIPE, stderr=PIPE, check=True)
# #         print("done opensemn")
# #         print("...Entering record in database")
# #         pushtodb(filename)
# #         f = open("logfile.txt", "a")
# #         f.write("End: "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\n")
# #         f.close()

# #     except:
# #         print("Something went wrong in "+filename)
# #         f = open("failed_uploads.txt", "a")
# #         f.write("Failed to upload "+filename+" at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n")
# #         f.close()
# #         #subprocess.call('http://127.0.0.1:/search-apps/api/index-web? uri=https:/s3.amazonaws.com/'+pdf_s3_bucket + '/' + filename + ".pdf", shell=True)
# f = open("logfile.txt", "a")
# f.write("==============================================================================\n")
# f.close()

# subprocess.call('sudo rm /home/ubuntu/*.json', shell=True)
# subprocess.call('sudo rm /home/ubuntu/backup_input/*', shell=True)
# subprocess.call('sudo rm /home/ubuntu/outputpdfs/*', shell=True)
# print("...Done")
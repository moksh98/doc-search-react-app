import os
from time import strftime, gmtime

from PIL import Image
from app.core.celery_app import celapp
from app.core.settings import settings
from app.database.elasticsearchadapter import SyncElasticSearchAdapter
from app.helper.celeryhelper import PdfCreator
from app.models.collections import *

import boto3
import pdf2image

from app.dependencies import get_redis


def error_handler(task_id):
    # handle the exception
    f = open(settings.FAILED_LOG, "a")
    f.write("Failed to upload " + task_id + " at " +
            strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n")
    f.close()
    print(f"Task {task_id} failed for")


def delete_files(filename):

    if os.path.exists(os.path.join(settings.FILE_STORE, filename + ".png")):
        os.remove(os.path.join(settings.FILE_STORE, filename + ".png"))

    if os.path.exists(os.path.join(settings.PDF_OUT_STORE, filename + ".pdf")):
        os.remove(os.path.join(settings.PDF_OUT_STORE, filename + ".pdf"))


def index_doc(filename, pdf_file, ocr_response, coll_info={}):
    awsuri = "https://" + settings.PDF_S3_BUCKET + \
        ".s3.amazonaws.com/" + pdf_file
    page_number = int(filename.split("_")[-1])

    coll_info["file_name"] = pdf_file
    coll_info["page_number"] = page_number
    coll_info["AWS_link"] = awsuri
    coll_info["content"] = ocr_response

    print(coll_info)

    sync_elastic = SyncElasticSearchAdapter()
    try:
        response = sync_elastic.index(coll_info, id=coll_info["file_name"])
        print(response)
    except Exception as e:
        raise Exception("DOCUMENT NOT INDEXED...ERROR OCCURED!!\n", e)


def upload_pdf(pdf_filename):
    print("...Uploading on S3")

    client = boto3.client("s3",
                          aws_access_key_id=settings.S3_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
                          region_name=settings.S3_REGION_NAME)

    client.upload_file(os.path.join(settings.PDF_OUT_STORE, pdf_filename),
                       settings.PDF_S3_BUCKET,
                       pdf_filename.split("/")[-1])

    print("...Uploaded on S3")


# Google Vision at this point allows images of size < 10 mb for OCR. # noqa: E501
# Hence this functions reduces the size of image greater than 10mb. # noqa: E501
def reduce_size(image_filename):
    if os.stat(os.path.join(settings.FILE_STORE, image_filename)).st_size < 10485760:
        print(f"...Not Reducing Size for {image_filename}")
        return
    else:
        print(f"...Reducing Size for {image_filename}")
        img = Image.open(os.path.join(settings.FILE_STORE, image_filename))
        max_size = (img.size[0], img.size[1])
        while os.path.getsize(os.path.join(settings.FILE_STORE, image_filename)) > 10485760:
            max_size = (int(max_size[0] * 0.8), int(max_size[1] * 0.8))
            img = img.resize(max_size, resample=Image.Resampling.LANCZOS)
            img.save(os.path.join(settings.FILE_STORE, image_filename))

    img.close()


# def create_thumbnail(fullname):
#     print(f"...Creating Thumbnail for {fullname}")
#     img = Image.open(os.path.join(settings.FILE_STORE, fullname))

#     thumb = img.convert("L")
#     thumb.thumbnail(size=(256, 256))

#     thumb.save(os.path.join(settings.THUMB_STORE, fullname), optimize=True)
#     print(f"Created Thumbnail for {fullname}.")


@celapp.task
def process_images(image_files, coll_info):
    project_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    font_path = os.path.join(project_dir, "static/arial.ttf")

    for image_filename in image_files:
        if os.path.splitext(image_filename)[0] in image_filename:
            filename = os.path.splitext(image_filename)[0]
            pdf_filename = filename + '.pdf'
            image_path = os.path.join(settings.FILE_STORE, image_filename)
            output_path = os.path.join(settings.PDF_OUT_STORE, pdf_filename)
            pdf_creator = PdfCreator(image_path, font_path, output_path=output_path)
            try:
                reduce_size(image_filename)
                ocr_response = pdf_creator.recognize_text()
                pdf_creator.create_pdf()
                upload_pdf(pdf_filename)
                index_doc(filename, pdf_filename, ocr_response, coll_info)
                delete_files(filename)
            except Exception as e:
                print(e)
                error_handler(process_images.request.id)


def get_image_in_batches(image_files):
    num_workers = len(celapp.control.inspect().active())
    batch_size = len(image_files) // num_workers
    batch_size = max(1, batch_size)
    batch_size = min(batch_size, 10)
    groups = [image_files[i:i + batch_size] for i in range(0, len(image_files), batch_size)]
    return groups


def delete_pdf_file(pdf_name):
    if os.path.exists(os.path.join(settings.PDF_IN_STORE, pdf_name)):
        os.remove(os.path.join(settings.PDF_IN_STORE, pdf_name))


def save_images(filename, images_from_path):
    image_files = []
    for pn in range(len(images_from_path)):
        image_filename = f"{os.path.splitext(os.path.basename(filename))[0]}_{pn + 1}.png"
        images_from_path[pn].save(os.path.join(settings.FILE_STORE, image_filename), "PNG")
        image_files.append(image_filename)
    return image_files


@celapp.task
def split_pdf_to_images(pdf_name, coll_info):
    images_from_path = pdf2image.convert_from_path(os.path.join(settings.PDF_IN_STORE, pdf_name))
    print("... Converted to image")
    image_files = save_images(pdf_name, images_from_path)
    print("... Saved image")
    delete_pdf_file(pdf_name)
    print("... Deleted PDF")
    groups = get_image_in_batches(image_files) 
    for images_group in groups:
        process_images.delay(images_group, coll_info)


if __name__ == "__main__":
    split_pdf_to_images.delay('/home/nsshah5/bayan_19160105_0_0.pdf')

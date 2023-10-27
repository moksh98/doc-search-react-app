from pydantic import BaseSettings
import os


class CommonSettings(BaseSettings):

    APP_NAME: str = "OCR Project Backend"
    DEBUG_MODE: bool = False
    SECRET_KEY: str
    GCV_CRED: str = "/home/ubuntu/keyfile/silken-buttress-274819-5ffbc93df39d.json"
    DISK_SPACE: int = 23222016


class UploadSettings(BaseSettings):
    FILE_STORE = os.path.join(os.path.expanduser("~"), 'images')
    # THUMB_STORE = os.path.join(os.path.expanduser("~"), 'thumbnails')
    PDF_IN_STORE = os.path.join(os.path.expanduser("~"), 'input_pdfs')
    PDF_OUT_STORE = os.path.join(os.path.expanduser("~"), 'output_pdfs')
    LOG_FILE = os.path.join(os.path.expanduser("~"), "logfile.txt")
    FAILED_LOG = os.path.join(os.path.expanduser("~"), "failed_uploads.txt")


class AWSSettings(BaseSettings):
    PDF_S3_BUCKET: str
    '''AWS s3 config'''
    S3_REGION_NAME: str = "us-east-1"
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str


class DatabaseSettings(BaseSettings):
    ''' Database settings '''
    DB_URL: str
    DB_PORT: int
    DATABASE: str
    DB_USER: str
    DB_PASS: str


class RedisConfig(BaseSettings):
    RD_HOST: str
    RD_PORT: int

class ElasticSearchSettings(BaseSettings):
    ES_SEARCH_INDEX = "kcldssearch"
    ES_HOST: str
    ES_USER: str
    ES_PASS: str


class Settings(CommonSettings, DatabaseSettings, ElasticSearchSettings, AWSSettings, UploadSettings, RedisConfig):
    class Config:
        env_file = ".env"

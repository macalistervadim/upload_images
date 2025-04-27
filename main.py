import os
from contextlib import asynccontextmanager

import boto3
from botocore.client import Config
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", "").split(",")

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_ENDPOINT}",
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    buckets = s3.list_buckets()
    if MINIO_BUCKET_NAME not in [
        bucket["Name"] for bucket in buckets.get("Buckets", [])
    ]:
        s3.create_bucket(Bucket=MINIO_BUCKET_NAME)

    # Настроить бакет как публичный
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{MINIO_BUCKET_NAME}/*"],
            },
        ],
    }
    s3.put_bucket_policy(
        Bucket=MINIO_BUCKET_NAME,
        Policy=str(policy).replace("'", '"'),
    )
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        s3.put_object(
            Bucket=MINIO_BUCKET_NAME,
            Key=file.filename,
            Body=content,
            ContentType=file.content_type,
        )
        file_url = f"http://{os.getenv('PUBLIC_MINIO_URL')}/{MINIO_BUCKET_NAME}/{file.filename}"
        return JSONResponse(content={"url": file_url})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

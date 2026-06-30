from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}

# async def create_upload_file(
#     file: Annotated[UploadFile, File(description="A file read as UploadFile")],
# ):

@app.post("/uploadfile/")

    return {"filename": file.filename}

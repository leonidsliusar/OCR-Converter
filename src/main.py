from converter.convert_exception import ConvertException
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from converter import entry
from utils import flush


app = FastAPI()

app.mount("/form", StaticFiles(directory="form"), name="static")


@app.get('/')
async def get_form():
    return FileResponse('form/index.html')


@app.post("/")
async def convert(
                    file: UploadFile,
                    background_tasks: BackgroundTasks
                ) -> FileResponse:
    try:
        text_file = await entry(file)
    except ConvertException:
        return await get_form()
    background_tasks.add_task(flush, text_file.path)
    headers = {"Content-Disposition": f"attachment; filename={text_file.name}"}
    return FileResponse(
        path=text_file.path,
        media_type="application/txt",
        filename=text_file.name,
        headers=headers
    )

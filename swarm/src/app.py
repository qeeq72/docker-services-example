from fastapi import FastAPI, UploadFile, Body, File
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
from time import time

from monkey_patch import set_monkey_patch
from db import create_table, get_description, save_description, get_all_descriptions
from s3 import create_backet, save_image, get_all_images


app = FastAPI(
    docs_url=None,
    redoc_url=None,
)
set_monkey_patch(app)


@app.post('/describe')
def describe(prompt: str = Body(embed=True), image: UploadFile = File(...)):
    tm1 = time()

    image_name = image.filename
    if get_description(prompt, image_name) is not None:
        return HTMLResponse(status_code=409)


    image_data = image.file.read()
    save_image(image_name, image_data)
    description = 'Hello world!'#'This is an amazing picture!'

    save_description(prompt, image_name, description)

    tm2 = time()
    return JSONResponse({
        'description': description,
        'duration': round(tm2-tm1, 2),
    })


@app.post('/descriptions')
def get_descriptions(image_name: str = Body(embed=True)):
    descriptions = get_all_descriptions(image_name)

    if descriptions:
        return JSONResponse({
            'descriptions': descriptions,
        })
    
    return HTMLResponse(status_code=404)


@app.get('/images')
def list_images():
    images = get_all_images()
    if images:
        return JSONResponse({
            'images': images,
        })
    
    return HTMLResponse(status_code=404)


@app.get('/healthcheck')
def make_healthcheck():
    return JSONResponse({'status': 'OK'})


if __name__ == '__main__':
    create_table()
    create_backet()
    uvicorn.run(app, host='0.0.0.0', port=80)

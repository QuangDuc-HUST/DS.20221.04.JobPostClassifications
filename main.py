# Importing Necessary modules
from src.app.core.utils.utils import *
from src.app.core.api import api
# from colabcode import ColabCode
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

# Declaring our FastAPI instance
app = FastAPI()


app.mount("/static", StaticFiles(directory="src/app/templates/static"), name="static")
# app.mount("/staging", StaticFiles(directory="src/app/staging"), name="staging")


# @app.on_event('startup')
# async def download_model_wandb():
#     download_model()

# @app.on_event("shutdown")
# def shutdown_event():
#     files = glob.glob('./app/staging/video/*.mp4')
#     for file in files:
#         print(file)
#         os.remove(file)


app.include_router(api.router)

# cc = ColabCode(port=12000, code=False)
# cc.run_app(app=app)

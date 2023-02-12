# Importing Necessary modules
from src.app.core.utils.utils import *
from src.app.core.api import api
# from colabcode import ColabCode
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI


# Declaring our FastAPI instance
app = FastAPI()


app.mount("/static", StaticFiles(directory="src/app/templates/static"), name="static")

app.include_router(api.router)

# cc = ColabCode(port=12000, code=False)
# cc.run_app(app=app)

# Importing Necessary modules
from fastapi import FastAPI
from models import *
import sys
sys.path.append('..')
from utils.utils import *
import uvicorn

# Declaring our FastAPI instance
app = FastAPI()


from pydantic import BaseModel

class request_body(BaseModel):
    description: str
    

@app.post('/predict-job')
def predict(data : request_body):
    input = [[
            data.description
    ]]

    clf = get_baseline_model()

    pred = clf.predict(preprocess_text(input))
    return {'class' : pred}

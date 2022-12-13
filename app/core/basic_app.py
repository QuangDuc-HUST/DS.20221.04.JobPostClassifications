# Importing Necessary modules
from fastapi import FastAPI
import uvicorn

# Declaring our FastAPI instance
app = FastAPI()

from pydantic import BaseModel

class request_body(BaseModel):
    sepal_length : float
    sepal_width : float
    petal_length : float
    petal_width : float
    

@app.post('/predict')
def predict(data : request_body):
    test_data = [[
            data.sepal_length, 
            data.sepal_width, 
            data.petal_length, 
            data.petal_width
    ]]
    # class_idx = clf.predict(test_data)[0]
    class_idx = 1
    return { 'class' : class_idx}

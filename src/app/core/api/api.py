from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse
from fastapi import Request, status, UploadFile, Form, File
from tempfile import NamedTemporaryFile
from src.app.core.utils.utils import *
# from app.core.constants.constants import *
from inference import predict
import traceback
import json


router = APIRouter()

templates = Jinja2Templates(directory="src/app/templates")

predict_label = None
softmax_res = None
des = None


@router.get("/")
async def main(request: Request):
    if predict_label is not None:
        return templates.TemplateResponse("predict_home.html", {"request": request, "res": predict_label[['label', 'softmax']].values.tolist(), "heading": ['Label', 'Prediction'], "des": des})
    else:
        return templates.TemplateResponse("predict_home.html", {"request": request, "res": [[None, 100]], "heading": ['Label', 'Prediction'], "des": des})


@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('src/app/templates/static/img/favicon.ico')


@router.post("/predict/")
async def predict_job(description: str = Form()):
    global predict_label, softmax_res, des

    res = None
    des = description
    
    with open("idx2label.json") as f:
        idx2label = json.load(f)
    print(idx2label)
    try:
        print("start")
        output = predict( {"description": description}, 'weights/BERTweights.pth')
        print(output)
        res = idx2label[str(output.argmax())]

        val, idx = torch.topk(torch.from_numpy(output), k=10)
        val, label_id = val.numpy().tolist(), idx.numpy().tolist()

        print('Predicted')
    except Exception as e:
        print("An error occured during prediction: ", traceback.format_exc())

    print(res)
    val, idx = torch.topk(torch.from_numpy(output), k=10)
    val, label_id = val.numpy().tolist(), idx.numpy().tolist()
    predict_label = pd.DataFrame({'label_id': label_id, 'softmax': [round(i * 100, 3) for i in val], 'label': [idx2label[str(i)] for i in label_id]})
    predict_label = predict_label.sort_values(by="softmax", ascending=False)
    predict_label.index = pd.RangeIndex(start=1, stop=11, step=1)

    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)

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
from src.app.core.utils.constants.constants import *

router = APIRouter()

templates = Jinja2Templates(directory="src/app/templates")

predict_label = None
softmax_res = None
des = None


@router.get("/")
async def main(request: Request):
    if predict_label is not None:
        return templates.TemplateResponse("predict_home.html", {"request": request, "res": predict_label[['label', 'softmax']].values.tolist(), "heading": ['Label', 'Prediction'], "des": des, "constants": LABEL_IDX})
    else:
        return templates.TemplateResponse("predict_home.html", {"request": request, "res": [[None, 100]], "heading": ['Label', 'Prediction'], "des": des, "constants": LABEL_IDX})


@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('src/app/templates/static/img/favicon.ico')


@router.post("/predict/")
async def predict_job(title: str = Form(),
                      description: str = Form(),
                      vacancies: str = Form(default=None),
                      min_salary: str = Form(default=None),
                      max_salary: str = Form(default=None),
                      age_range: str = Form(default=None),
                      gender: str = Form(default=None),
                      benefits: str = Form(default=None),
                      job_location: str = Form(default=None),
                      salary_type: str = Form(default=None),
                      skills: str = Form(default=None),
                      contract_type: str = Form(default=None),
                      education_requirements: str = Form(default=None),
                      experience_requirements: str = Form(default=None)):

    print(locals().items())
    all_fields = list(locals().values())

    print([i is not None for i in all_fields])
    print(all_fields)

    if all([i is None for i in all_fields[2:]]):
        print("BERT")
        print(all([i is not None for i in all_fields]))
        input = {'title': title,
                 'description': description}
    elif all([i is not None for i in all_fields]):
        print("COMBERT")
        input = {'title': title,
                 'description': description,
                 'vacancies': int(vacancies) if vacancies is not None else None,
                 'min_salary': int(min_salary) if min_salary is not None else None,
                 'max_salary': int(max_salary) if max_salary is not None else None,
                 'age_range': age_range,
                 'gender': gender,
                 'benefits': benefits,
                 'job_location': job_location,
                 'salary_type': salary_type,
                 'skills': skills,
                 'contract_type': contract_type,
                 'education_requirements': education_requirements,
                 'experience_requirements': experience_requirements,
                 }

    global predict_label, softmax_res, des

    res = None
    des = description

    try:
        print("start")
        output = predict(input, 'weights/', "config.json")
        print(output)
        res = JOB_LABEL[str(output.argmax())]

        val, idx = torch.topk(torch.from_numpy(output), k=10)
        val, label_id = val.numpy().tolist(), idx.numpy().tolist()

        print('Predicted')
    except Exception as e:
        print("An error occured during prediction: ", traceback.format_exc())

    print(res)
    val, idx = torch.topk(torch.from_numpy(output), k=10)
    val, label_id = val.numpy().tolist(), idx.numpy().tolist()
    predict_label = pd.DataFrame({'label_id': label_id, 'softmax': [round(i * 100, 3) for i in val], 'label': [JOB_LABEL[str(i)] for i in label_id]})
    predict_label = predict_label.sort_values(by="softmax", ascending=False)
    predict_label.index = pd.RangeIndex(start=1, stop=11, step=1)

    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)

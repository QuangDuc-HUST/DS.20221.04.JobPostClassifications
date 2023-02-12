# DS.20221.04.JobPostClassifications
Data Science Project - DANDL

To run this project, you first need to download the all weights file of models to the `weights` folder. [Here](https://drive.google.com/drive/u/1/folders/1HsjeWkmx0Iy_Gd4V7jM08MpUmdJnumjs) is the download link.

Then simply run the following command to start the __FastAPI__ webserver and use our UI 
```
uvicorn main:app
```

_Notice_: there are only __two__ way for you to input the information: 
- Fill in all the blanks and select options of all dropdown menus to use __COMBERT__ model
- Only fill in two blanks: description and title to use __BERT__ model
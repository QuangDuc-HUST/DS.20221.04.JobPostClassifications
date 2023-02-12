import json

LABEL_IDX = {
    'AGE_RANGE': json.load(open('idx2label/age_range_label2idx.json', 'r')),

    'CONTRACT_TYPE': json.load(open('idx2label/contract_type_label2idx.json', 'r')),

    'EDUCATION': json.load(open('idx2label/education_requirements_label2idx.json', 'r')),

    'EXPERIENCE': json.load(open('idx2label/experience_requirements_label2idx.json', 'r')),

    'REGION': json.load(open('idx2label/location_label2idx.json', 'r')),

    'SALARY_TYPE': json.load(open('idx2label/salary_type_label2idx.json', 'r')),

    'GENDER': ["Không yêu cầu", "Name", "Nữ"]
}

JOB_LABEL = json.load(open('idx2label/job_type_idx2label.json', 'r'))

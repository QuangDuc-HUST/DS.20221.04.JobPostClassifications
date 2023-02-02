import os
import json
import torch
import re
import underthesea as uts
from transformers import AutoTokenizer, logging
logging.set_verbosity_error()


VIETNAMESE_STOPWORD = []

with open(os.path.join("auxiliary", "vietnamese-stopwords.txt" ), encoding="utf-8") as f:
    VIETNAMESE_STOPWORD = [word.strip() for word in f.readlines()]


def process_input(user_input, max_len_text):
    """
    Input:

    user_input: dictionary like input_dict = {"description" : "duc dep trai", "title": "hehe", "salary": 100000, ...}

    """

    assert isinstance(user_input, dict), "Not corrected type."

    assert user_input["description"] is None or user_input["title"] is None, "There is none value in description and title field" # Not input all fields
    
    # Check if other field is None
    is_none_all = True
    for key, value in  user_input.items():
        if value is not None:
            is_none_all = False
            break
    

    tokenizer =  AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)


    text_field =  user_input["title"] + " " + user_input["description"] 

    processed_text_field = process_text_sentence(text_field, tokenizer, max_len_text)
    

    if is_none_all:
        # Only text fields
        processed_numeric_field = None
    
    else:

        nontextpreprocess = NonTextDataPreprocess(user_input, is_infer=True)

        preprocess_numeric_input = nontextpreprocess.run()

        print(sorted(preprocess_numeric_input.keys()))

        processed_numeric_field = torch.tensor([preprocess_numeric_input[key] for key in sorted(preprocess_numeric_input.keys())]).unsqueeze(0)


    processed_input = processed_text_field, processed_numeric_field 

    return processed_input



def process_text_sentence(string, tokenizer, max_len):


    def split_word(string):
        new_string = ''
        for i in range(len(string) - 1):
            if string[i].isupper() and string[i + 1].islower():
                new_string += ' ' + string[i]
            else:
                new_string += string[i]
        return new_string + string[-1]

    def remove_forms(string):
        lst = []
        for x in string.split(' '):
            if 'http' not in x:
                lst.append(x)
        return ' '.join(lst)

    def remove_email(string):
        lst = []
        for x in string.split(' '):
            if '@' not in x:
                lst.append(x)
        return ' '.join(lst)

    def clean_str(string):
        string = re.sub("[^aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0-9]", " ", string)
        lst = []
        for x in string.split(' '):
            if x != '':
                lst.append(x)
        return ' '.join(lst)

    def remove_url(string):
        url_pattern = re.compile(r'http\S+')
        return url_pattern.sub(r'', string)

    def remove_stopword(string):
        return " ".join(x for x in string.split() if x not in VIETNAMESE_STOPWORD)

    result = string.replace("(<br/>)", "")
    result = result.replace('(<a).*(>).*(</a>)', '')
    result = result.replace('(&amp)', '')
    result = result.replace('(&gt)', '')
    result = result.replace('(&lt)', '')
    result = result.replace('(\xa0)', ' ')  
    result = result.replace('&nbsp;', ' ')  
    result = result.replace('&nbsp', ' ')   
    result = result.replace('\n', ' ')
    # result = remove_in_parentheses(result)
    result = split_word(result)
    result = remove_email(result)
    result = remove_forms(result)
    result = result.lower()
    result = clean_str(result)
    result = remove_url(result)
    result = uts.text_normalize(result)
    result = remove_stopword(result)

    encoding = tokenizer.encode_plus(
            result,
            truncation=True,
            add_special_tokens=True,
            max_length=max_len,
            padding='max_length',
            return_attention_mask=True,
            return_token_type_ids=False,
            return_tensors='pt',
        )


    return  {
            'input_ids': encoding['input_ids'].flatten().unsqueeze(0),
            'attention_masks': encoding['attention_mask'].flatten().unsqueeze(0),
        }


class NonTextDataPreprocess():

    def __init__(self, inputs: dict(), param_file='auxiliary/mapping_dict.json', is_infer=False): 
        self.dic = inputs

        self.__loading_data(param_file)
        self.__threshold_salary = 1200000  # 1,200,000

        self.result_dic = {}

        self.is_infer = is_infer

    def run(self): 
        '''
        Magic. 
        Cleaning, pre-processing data
        Return: dict()
        '''
        self.__convert_age()

        # self.__convert_column('education_requirements', self.convert_edu, 'Không yêu cầu')
        self.__convert_column('experience_requirements', self.convert_exp, 'Không yêu cầu')
        self.__convert_column('contract_type', self.convert_contract, 'Fulltime')
        self.__convert_column('salary_type', self.convert_salary_type, 'monthly')
        
        self.__normalized_column('min_salary', self.min_salary_lmbda, self.mean_min_salary)
        self.__normalized_column('max_salary', self.max_salary_lmbda, self.mean_max_salary)
        self.__normalized_column('vacancies', self.vacancies_lmbda, 1)
        
        self.__encode_location()

        if self.is_infer:
            self.__encode_to_idx()

        return self.result_dic

    def __loading_data(self, param_file: str): 
        with open(param_file, encoding='utf-8') as json_file:
            data = json.load(json_file)
            
            # Load dictionaries and data structures
            self.convert_contract = data['CONTRACT_TYPE_DICT']
            self.convert_salary_type = data['SALARY_TYPE_CONVERTER']
            self.convert_edu = data['EDUCATION_REQUIREMENTS_CONVERTER']
            self.convert_exp = data['EXPERIENCE_REQUIREMENTS_CONVERTER']
            self.regions = data['regions']

            self.location_convert_dict = data['LOCATION_CONVERTER']
            
            # Load parameters
            self.min_salary_lmbda = data['min_salary_lmbda']
            self.max_salary_lmbda = data['max_salary_lmbda']
            self.vacancies_lmbda = data['vacancies_lmbda']
            self.mean_min_salary = data['mean_min_salary']
            self.mean_max_salary = data['mean_max_salary']

    def __normalized_column(self, column_name, lmbda, mean):        #oce
        assert type(self.dic[column_name]) == int, f'Type {column_name} is not integer (int)'
        x = self.dic[column_name]
        if 'salary' in column_name:  
            x = x if x > self.__threshold_salary else mean 
        else: 
            x = max(x, 1)

        self.result_dic[f'normalized_{column_name}'] = (x** lmbda - 1) /lmbda

    def __convert_column(self, column_name:str, col_dict: dict, handle_missing: str):    #oce
        old_value = self.dic[column_name]
        if old_value is None: 
            old_value = handle_missing
        self.result_dic[column_name] = col_dict.get(old_value, old_value)
        
    def __convert_age(self):       
                 #oce
        def convert_age(age: int):
            if age in range(18, 20): 
                return '18-19'
            elif age in range(20, 25): 
                return '20-24'
            elif age in range(25, 30): 
                return '25-29'
            elif age in range(30, 35): 
                return '30-35'
            return 'over 35'
        
        old_value = self.dic['age_range']
        if old_value[:2].isnumeric():
            new_value = int(old_value[:2])
            new_value = new_value if new_value > 17 else 20
            new_value = convert_age(int(old_value[:2]))
        else: 
            new_value = 'Không yêu cầu'
        
        self.result_dic['age_range'] = new_value

    def __encode_location(self):        #oce
        job_location = self.dic['job_location'].lower()
        location = None

        self.regions = [region.lower() for region in self.regions]
        for loc in self.regions: 
            if loc in job_location: 
                location = loc

        if not location: 
            for k, v in self.location_convert_dict.items():
                if k in job_location: 
                    location = v
                    break 
            else: 
                location = 'không xác định'

        self.result_dic['location'] = location
    
    def __encode_to_idx(self, folder='idx2label/'):
        for key in self.result_dic:
            json_file_key = os.path.join(folder, f"{key}_label2idx.json")
            if os.path.exists(json_file_key):
                with open(json_file_key) as f:
                    key_label2idx = json.load(f)
            
                self.result_dic[key] = key_label2idx[self.result_dic[key]]

if __name__ == '__main__':
    ## Testing

    original_input = {'id': 101883361,
                    'company_id': 24261353,
                    'title': 'Nhân Viên Tư Vấn Tuyển Sinh',
                    'post_time': '2022-12-10 00:36:41',
                    'description': '- Tìm kiếm, xây dựng & phát triển nguồn khách hàng tiềm năng\n- Ghi nhận và tìm hiểu nhu cầu của học viên theo quy trình tư vấn\n- Tư vấn chương trình đào tạo phù hợp\n- Theo dõi tình hình học tập của học viên và thực hiện các dịch vụ chăm sóc học viên\n- Ghi nhận, xử lý và báo cáo với cấp quản lý trực tiếp về các phát sinh liên quan đến học viên/ phụ huynh\n- Thông báo cho học viên và phụ huynh các hoạt động ngoại khóa, hội thảo và thông tin du học nhằm thu hút học viên mới và chăm sóc học viên đang học',
                    'vacancies': 1,
                    'min_salary': 8000000,
                    'max_salary': 10000000,
                    'age_range': '20-',
                    'gender': 'Nữ',
                    'benefits': 'Phụ cấp, tham gia BHXH, tăng lương',
                    'job_location': 'Xã An Ninh Đông, Huyện Đức Hòa, Long An',
                    'salary_type': 'Theo tháng',
                    'region': 'Long An',
                    'url': 'https://www.vieclamtot.com/viec-lam-huyen-duc-hoa-long-an/101883361.htm',
                    'created_time': '2023-01-02 15:57:57',
                    'updated_time': '2023-01-02 15:57:57',
                    'skills': 'Không yêu cầu',
                    'job_type': 'Cham soc khach hang',
                    'contract_type': 'Làm theo ca',
                    'education_requirements': 'Cấp 3',
                    'experience_requirements': '< 1 năm',
                    'website': 'www.vieclamtot.com'}

    # print(process_input({"description": orginal_text}, 125))    
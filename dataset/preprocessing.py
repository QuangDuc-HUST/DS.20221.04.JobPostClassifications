import os
import re
import json
import underthesea as uts

VIETNAMESE_STOPWORD = []

with open(os.path.join("auxiliary", "vietnamese-stopwords.txt" ), encoding="utf-8") as f:
    VIETNAMESE_STOPWORD = [word.strip() for word in f.readlines()]

# Text Data Preprocess (Processing Test Data)
def process_text_sentence(string, is_title=False):
    
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
    if not is_title:
        result = remove_stopword(result)

    return result

class NonTextDataPreprocess():

    def __init__(self, inputs: dict(), param_file='auxiliary/mapping_dict.json'): 
        self.dic = inputs

        self.__loading_data(param_file)
        self.__threshold_salary = 1200000  # 1,200,000

        self.result_dic = {}

    def run(self): 
        '''
        Magic. 
        Cleaning, pre-processing data
        Return: dict()
        '''
        self.__convert_age()

        self.__convert_column('education_requirements', self.convert_edu, 'Không yêu cầu')
        self.__convert_column('experience_requirements', self.convert_exp, 'Không yêu cầu')
        self.__convert_column('contract_type', self.convert_contract, 'Fulltime')
        self.__convert_column('salary_type', self.convert_salary_type, 'monthly')
        
        self.__normalized_column('min_salary', self.min_salary_lmbda, self.mean_min_salary)
        self.__normalized_column('max_salary', self.max_salary_lmbda, self.mean_max_salary)
        self.__normalized_column('vacancies', self.vacancies_lmbda, 1)
        
        self.__encode_location()

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
        self.dic[column_name] = col_dict.get(old_value, old_value)
        
        
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
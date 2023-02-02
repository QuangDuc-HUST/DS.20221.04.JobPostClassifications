import os


import re
import underthesea as uts
from transformers import AutoTokenizer, logging
logging.set_verbosity_error()


def process_text_sentence(string, tokenizer, max_len):

    VIETNAMESE_STOPWORD = []

    with open(os.path.join("auxiliary", "vietnamese-stopwords.txt" ), encoding="utf-8") as f:
        VIETNAMESE_STOPWORD = [word.strip() for word in f.readlines()]


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


def process_input(user_input, max_len):
    """
    Input:

    user_input: dictionary like input_dict = {"description" : "duc dep trai", "title": "hehe", "salary": 100000, ...}

    """

    tokenizer =  AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)


    description_field = user_input["description"]

    processed_description_field = process_text_sentence(description_field, tokenizer, max_len)
    
    processed_input = processed_description_field

    return processed_input


if __name__ == '__main__':
    ## Testing
    orginal_text = "Hélô  😆"
    print(orginal_text)
    print(process_input({"description": orginal_text}, 125))    
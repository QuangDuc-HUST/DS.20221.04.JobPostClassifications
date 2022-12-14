import re
import string
import underthesea as uts
import urllib.request


vnese_stopwords = urllib.request.urlopen('https://raw.githubusercontent.com/stopwords/vietnamese-stopwords/master/vietnamese-stopwords.txt')
vnese_stopwords_dash = urllib.request.urlopen('https://raw.githubusercontent.com/stopwords/vietnamese-stopwords/master/vietnamese-stopwords.txt')

# STOPWORD

VIETNAMESE_STOPWORD = [word.strip() for word in vnese_stopwords]
VIETNAMESE_STOPWORD_DASH = [word.strip() for word in vnese_stopwords_dash]

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(" ", string)


def preprocess_text(series_text_field):

    PUNCT_TO_REMOVE = string.punctuation
    def remove_punctuation(text):
        """custom function to remove the punctuation"""
        return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))


    result = series_text_field.str.replace("(<br/>)", "",  regex=True)
    result = result.str.replace('(<a).*(>).*(</a>)', '',  regex=True)
    result = result.str.replace('(&amp)', '',  regex=True)
    result = result.str.replace('(&gt)', '',  regex=True)
    result = result.str.replace('(&lt)', '',  regex=True)
    result = result.str.replace('(\xa0)', ' ',  regex=True)  
    result = result.str.replace('&nbsp;', ' ',  regex=True)  
    result = result.str.replace('&nbsp', ' ',  regex=True) 

    result = result.str.replace('•', ' ',  regex=True)   
    result = result.str.replace('\n', ' ',  regex=True)
    result = result.str.replace('·', ' ', regex=True)
    result = result.str.replace('🫐', ' ', regex=True)
    result = result.str.replace('…', ' ', regex=True)
    result = result.str.replace("—", ' ', regex=True)
    result = result.str.replace(" ̀", ' ', regex=True)
    result = result.str.replace(" ̛", ' ', regex=True)
    result = result.str.replace(" ̣", ' ', regex=True)
    result = result.str.replace(" ̣", ' ', regex=True)
    result = result.str.replace(" ", ' ', regex=True)
    result = result.str.replace("-", ' ', regex=True)
    result = result.str.lower()
    result = result.str.strip()

    result = result.apply(remove_emoji)
    result = result.apply(uts.text_normalize)

    result = result.apply(lambda text: remove_punctuation(text))
    result = result.apply(uts.text_normalize)
    
    return result
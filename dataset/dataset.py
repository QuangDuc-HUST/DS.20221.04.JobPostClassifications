
import torch
from torch.utils.data import Dataset

import pandas as pd


class JobDataset(Dataset):

   def __init__(self, x, y):
      self.x = x
      self.y = y
      
   def __len__(self):
      return len(self.x)
      
   def __getitem__(self, idx):
      text = self.x[idx]
      label = self.y.iloc[idx]

      return text, label



class JobBERTDataset(Dataset):

    def __init__(self, df_x, df_y, tokenizer, max_len):

        self.df_x = df_x
        self.df_y = df_y

        self.max_len = max_len
        self.tokenizer = tokenizer


    def __len__(self):
        return len(self.df_y)

    def __getitem__(self, index):
        """
        To customize dataset, inherit from Dataset class and implement
        __len__ & __getitem__
        __getitem__ should return 
            data:
                input_ids
                attention_masks
                text
                targets
        """
        text, label = self.df_x.iloc[index], self.df_y.iloc[index]

        # Encode_plus will:
        # (1) split text into token
        # (2) Add the '[CLS]' and '[SEP]' token to the start and end
        # (3) Truncate/Pad sentence to max length
        # (4) Map token to their IDS
        # (5) Create attention mask
        # (6) Return a dictionary of outputs

        encoding = self.tokenizer.encode_plus(
            text,
            truncation=True,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_attention_mask=True,
            return_token_type_ids=False,
            return_tensors='pt',
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_masks': encoding['attention_mask'].flatten(),
        }, torch.tensor(label, dtype=torch.long)


class ComJobDataset(Dataset):

   def __init__(self, x, y, tokenizer, seq_len, numeric_cols = []):

      self.x = x
      self.y = y 
    
      self.seq_len = seq_len

      self.tokenizer = tokenizer
      self.x_text = self.x['title']  + ' ' + self.x['description']
      self.x_num = pd.get_dummies(self.x[numeric_cols]).to_numpy()


   def __len__(self):
      return len(self.y)
      
   def __getitem__(self, idx):

      converted_text = self.tokenizer(self.x_text.iloc[idx], self.seq_len)
      converted_numeric = self.x_num[idx]

      label = self.y.iloc[idx]

      return (converted_text, converted_numeric), label


class ComJobBERTDataset(Dataset):

   def __init__(self, x, y, tokenizer, seq_len, numeric_cols = []):

      self.x = x
      self.y = y 
    
      self.seq_len = seq_len

      self.tokenizer = tokenizer
      self.x_text = self.x['title'] + ' ' + self.x['description']
      self.x_num = pd.get_dummies(self.x[numeric_cols]).to_numpy()


   def __len__(self):
      return len(self.y)
      
   def __getitem__(self, idx):
        
    text = self.x_text.iloc[idx]
    numeric = self.x_num[idx]

    label = self.y.iloc[idx]


    encoding = self.tokenizer.encode_plus(
        text,
        truncation=True,
        add_special_tokens=True,
        max_length=self.max_len,
        padding='max_length',
        return_attention_mask=True,
        return_token_type_ids=False,
        return_tensors='pt',
    )
    
    return ({
        'input_ids': encoding['input_ids'].flatten(),
        'attention_masks': encoding['attention_mask'].flatten(),
    }, numeric), torch.tensor(label, dtype=torch.long)


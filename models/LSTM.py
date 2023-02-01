## Source: https://github.com/FernandoLpz/Text-Classification-LSTMs-PyTorch

import torch
from torch import nn

from utils.pytorch import get_training_device

class LSTMModel(nn.ModuleList):

    def __init__(self, hidden_dim, lstm_layers, num_words, drop_out_rate, num_classes, is_bidirectional):
        super(LSTMModel, self).__init__()
        
        self.hidden_dim = hidden_dim
        self.LSTM_layers = lstm_layers
        self.num_words = num_words 
        self.num_classes = num_classes
        self.is_bidirectional = is_bidirectional
        
        self.dropout = nn.Dropout(drop_out_rate)
  
        self.embedding = nn.Embedding(self.num_words + 1, self.hidden_dim, padding_idx=0)
        self.lstm = nn.LSTM(input_size=self.hidden_dim, hidden_size=self.hidden_dim, num_layers=self.LSTM_layers, batch_first=True, bidirectional=self.is_bidirectional)

        if is_bidirectional:
            self.fc1 = nn.Linear(in_features=self.hidden_dim*2, out_features=1024)
        else:
            self.fc1 = nn.Linear(in_features=self.hidden_dim, out_features=1024)

        self.fc2 = nn.Linear(1024, self.num_classes)
        
    def forward(self, x):
    
        h = torch.zeros((self.LSTM_layers * 2 if self.is_bidirectional else  self.LSTM_layers,  x.size(0) , self.hidden_dim ), device=get_training_device(False))
        c = torch.zeros((self.LSTM_layers * 2 if self.is_bidirectional else  self.LSTM_layers, x.size(0) , self.hidden_dim ), device=get_training_device(False))
        
        torch.nn.init.xavier_normal_(h)
        torch.nn.init.xavier_normal_(c)

        out = self.embedding(x)

        out, (hidden, cell) = self.lstm(out, (h, c))
  
        out = self.dropout(out)
  
        out = torch.relu_(self.fc1(out[:,-1,:]))
  
        out = self.dropout(out)
  
        out = self.fc2(out)

        return out
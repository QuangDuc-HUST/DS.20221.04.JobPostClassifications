from transformers import AutoModel

from torch import nn

# Source

class PhoBERTModel(nn.Module):
  
    def __init__(self, num_classes):

        super(PhoBERTModel, self).__init__()
        self.bert = AutoModel.from_pretrained("vinai/phobert-base")
        self.drop = nn.Dropout(p=0.3)
        self.fc = nn.Linear(self.bert.config.hidden_size, num_classes)
        nn.init.normal_(self.fc.weight, std=0.02)
        nn.init.normal_(self.fc.bias, 0)

    def forward(self, x):

        input_ids = x['input_ids']
        attention_masks = x['attention_masks']        

        _, output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_masks,
            return_dict=False # Dropout will errors if without this
        )

        x = self.drop(output)
        x = self.fc(x)

        return x



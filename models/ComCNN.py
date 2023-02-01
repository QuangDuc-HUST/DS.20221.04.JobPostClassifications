import math

import torch
from torch import nn

#https://towardsdatascience.com/how-to-combine-textual-and-numerical-features-for-machine-learning-in-python-dc1526ca94d9

class CombinationCNNModel(nn.ModuleList):

    def __init__(self, seq_len, num_words,  embedding_size, out_size, stride, in_dimensions, dense_size, num_class):
        super(CombinationCNNModel, self).__init__()

        # Parameters regarding text preprocessing
        self.seq_len = seq_len
        self.num_words = num_words
        self.embedding_size = embedding_size
        self.dense_size = dense_size
        self.in_dimensions = in_dimensions
                
        # CNN parameters definition
        # Kernel sizes
        self.kernel_1 = 2
        self.kernel_2 = 3
        self.kernel_3 = 4
        self.kernel_4 = 5
        
        # Output size for each convolution
        self.out_size = out_size
        # Number of strides for each convolution
        self.stride = stride
        
        # Embedding layer definition
        self.embedding = nn.Embedding(self.num_words + 1, self.embedding_size, padding_idx=0)
        
        # Convolution layers definition
        self.conv_1 = nn.Conv1d(self.seq_len, self.out_size, self.kernel_1, self.stride)
        self.conv_2 = nn.Conv1d(self.seq_len, self.out_size, self.kernel_2, self.stride)
        self.conv_3 = nn.Conv1d(self.seq_len, self.out_size, self.kernel_3, self.stride)
        self.conv_4 = nn.Conv1d(self.seq_len, self.out_size, self.kernel_4, self.stride)
        
        # Max pooling layers definition
        self.pool_1 = nn.MaxPool1d(self.kernel_1, self.stride)
        self.pool_2 = nn.MaxPool1d(self.kernel_2, self.stride)
        self.pool_3 = nn.MaxPool1d(self.kernel_3, self.stride)
        self.pool_4 = nn.MaxPool1d(self.kernel_4, self.stride)
        
        # Fully connected layer definition
        self.fc_1 = nn.Linear(self.in_features_fc(), self.dense_size)
        self.fc_2 = nn.Linear(self.dense_size +  self.in_dimensions, num_class)
  
        
    def in_features_fc(self):
        # Calcualte size of convolved/pooled features for convolution_1/max_pooling_1 features
        out_conv_1 = ((self.embedding_size - 1 * (self.kernel_1 - 1) - 1) / self.stride) + 1
        out_conv_1 = math.floor(out_conv_1)
        out_pool_1 = ((out_conv_1 - 1 * (self.kernel_1 - 1) - 1) / self.stride) + 1
        out_pool_1 = math.floor(out_pool_1)
        
        # Calcualte size of convolved/pooled features for convolution_2/max_pooling_2 features
        out_conv_2 = ((self.embedding_size - 1 * (self.kernel_2 - 1) - 1) / self.stride) + 1
        out_conv_2 = math.floor(out_conv_2)
        out_pool_2 = ((out_conv_2 - 1 * (self.kernel_2 - 1) - 1) / self.stride) + 1
        out_pool_2 = math.floor(out_pool_2)
        
        # Calcualte size of convolved/pooled features for convolution_3/max_pooling_3 features
        out_conv_3 = ((self.embedding_size - 1 * (self.kernel_3 - 1) - 1) / self.stride) + 1
        out_conv_3 = math.floor(out_conv_3)
        out_pool_3 = ((out_conv_3 - 1 * (self.kernel_3 - 1) - 1) / self.stride) + 1
        out_pool_3 = math.floor(out_pool_3)
        
        # Calcualte size of convolved/pooled features for convolution_4/max_pooling_4 features
        out_conv_4 = ((self.embedding_size - 1 * (self.kernel_4 - 1) - 1) / self.stride) + 1
        out_conv_4 = math.floor(out_conv_4)
        out_pool_4 = ((out_conv_4 - 1 * (self.kernel_4 - 1) - 1) / self.stride) + 1
        out_pool_4 = math.floor(out_pool_4)
        
        # Returns "flattened" vector (input for fully connected layer)
        return (out_pool_1 + out_pool_2 + out_pool_3 + out_pool_4) * self.out_size
        
        
        
    def forward(self, x_batch):

        # Sequence of tokes is filterd through an embedding layer

        x_text_in, x_num_in = x_batch

        x_text = self.embedding(x_text_in)
        
        # Convolution layer 1 is applied
        x1 = self.conv_1(x_text)
        x1 = torch.relu(x1)
        x1 = self.pool_1(x1)
        
        # Convolution layer 2 is applied
        x2 = self.conv_2(x_text)
        x2 = torch.relu((x2))
        x2 = self.pool_2(x2)
    
        # Convolution layer 3 is applied
        x3 = self.conv_3(x_text)
        x3 = torch.relu(x3)
        x3 = self.pool_3(x3)
        
        # Convolution layer 4 is applied
        x4 = self.conv_4(x_text)
        x4 = torch.relu(x4)
        x4 = self.pool_4(x4)
        
        # The output of each convolutional layer is concatenated into a unique vector
        union_text = torch.cat((x1, x2, x3, x4), 2)
        union_text = union_text.reshape(union_text.size(0), -1)

        

        # The "flattened" vector is passed through a fully connected layer


        dense_out = self.fc_1(union_text)

        concat_layer = torch.concat([dense_out, x_num_in], dim =1)

        out = self.fc_2(concat_layer)
        

        return out.squeeze()
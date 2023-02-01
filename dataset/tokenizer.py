from copy import deepcopy
import nltk

import numpy as np


class JobTokenizationClass(object):
  
  def __init__(self):

    self.text_raw = None
    self.split_word_raw = None
    self.vocabulary = None

    self.x_tokenized = []

    self.results = []

    
  def load_data(self, df_data):
 
    self.text_raw = deepcopy(df_data)

    self.split_word_raw = None


  def text_split(self):
    
    assert self.text_raw is not None
    
    self.split_word_raw = [x.split() for x in self.text_raw]

  def build_vocabulary(self, num_words):
    
    assert self.vocabulary is None
    assert self.split_word_raw is not None

    self.vocabulary = dict()
    fdist = nltk.FreqDist()
    
    for sentence in self.split_word_raw:
      for word in sentence:
        fdist[word] += 1
        
    common_words = fdist.most_common(num_words)
    
    for idx, word in enumerate(common_words):
      self.vocabulary[word[0]] = (idx+1)

  def __call__(self, seq, seq_len_encoder):
      assert isinstance(seq, str)

      return self.get_tokenize_sentence(seq, seq_len_encoder)

  def get_tokenize_sentence(self, seq, seq_len_encoder):
        assert self.vocabulary is not None  
        
        split_word_raw = seq.split()
        
        result = []

        for word in split_word_raw:
            if word in self.vocabulary.keys():
                result.append(self.vocabulary[word])
            if len(result) >= seq_len_encoder:
                break

        pad_idx = 0

        while len(result) < seq_len_encoder:
            result.insert(len(result), pad_idx) 

        return np.array(result)

  def get_tokenize(self, seq_len):

    assert self.vocabulary is not None

    self.x_tokenized = []
    self.results = []

    if self.split_word_raw is None:
      self.text_split()

    for sentence in self.split_word_raw:
      temp_sentence = list()

      for word in sentence:
        if word in self.vocabulary.keys():
          temp_sentence.append(self.vocabulary[word])
        if len(temp_sentence) >= seq_len:
            break

      self.x_tokenized.append(temp_sentence)

      pad_idx = 0
    
    for sentence in self.x_tokenized:

      while len(sentence) < seq_len:
        sentence.insert(len(sentence), pad_idx)
      
      self.results.append(sentence)
      
    self.results = np.array(self.results)

    return self.results
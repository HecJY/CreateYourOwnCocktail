import torch
import torch.nn as nn
import numpy as np
from torch.autograd import Variable
from torch.optim import SGD
import torch.nn.functional as F

class CBOW(torch.nn.Module):

    def __init__(self, vocab_size, embedding_size, context_size):
        super(CBOW, self).__init__()
        #initialization
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.context_size = context_size

        #create the word embeddings
        self.embeddings = nn.Embedding(self.vocab_size, self.embedding_size)

        #the linear function, the input will be the size of emd * the ctx_size
        self.lin1 = nn.Linear(self.embedding_size, 300)
        self.lin2 = nn.Linear(300, self.vocab_size)

    def forward(self, inp):
        out = sum(self.embeddings(inp)).view(1, -1)
        out = self.lin1(out)
        out = F.relu(out)
        out = self.lin2(out)
        out = F.log_softmax(out, dim=-1)
        return out

    def get_word_vector(self, word_idx):
        word = Variable(torch.LongTensor([word_idx]))
        return self.embeddings(word).view(1, -1)



import torch
import torch.nn as nn
import numpy as np
from torch.autograd import Variable
from torch.optim import SGD
import torch.nn.functional as F


CONTEXT_SIZE = 4
EMBEDDING_DIM = 300
EPOCH = 20
VERVOSE = 5

class CBOW(torch.nn.Module):

    def __init__(self, vocab_size, embedding_size, context_size):
        super(CBOW, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.context_size = context_size
        self.embeddings = nn.Embedding(self.vocab_size, self.embedding_size)
        # return vector size will be context_size*2*embedding_size
        self.lin1 = nn.Linear(self.context_size * 2 * self.embedding_size, 512)
        self.lin2 = nn.Linear(512, self.vocab_size)

    def forward(self, inp):
        out = self.embeddings(inp).view(1, -1)
        out = out.view(1, -1)
        out = self.lin1(out)
        out = F.relu(out)
        out = self.lin2(out)
        out = F.log_softmax(out, dim=1)
        return out

    def get_word_vector(self, word_idx):
        word = Variable(torch.LongTensor([word_idx]))
        return self.embeddings(word).view(1, -1)



def get_percentage(cbow, unique_vocab, word_to_idx, source1, source2):
    # test word similarity
    word_1 = unique_vocab[3]
    word_2 = unique_vocab[3]

    word_1_vec = cbow.get_word_vector(word_to_idx[word_1])[0]
    word_2_vec = cbow.get_word_vector(word_to_idx[word_2])[0]

    word_similarity = (word_1_vec.dot(word_2_vec) / (torch.norm(word_1_vec) * torch.norm(word_2_vec))).data.numpy()
    print("Similarity between '{}' & '{}' : {:0.4f}".format(word_1, word_2, word_similarity))






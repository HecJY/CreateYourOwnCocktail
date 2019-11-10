import grad2grad
import grad2tech
import gradTech2amount
import load_cocktail_recp
import cbow_recp
import sys
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

def main():
    ctx_size = input("Please enter the number of sources you want to use")
    main_source = input("Please enter the sources you want them in the cocktail recipe, please enter them with ',' to separate")


    #first, load the information from the database
    (g2g, g2a, g2t) = load_cocktail_recp.grad_grad()

    #second, feed the grad2grad in and train the model
    g2g_mod = g2g_mod_operations(g2g)

    #third, feed the grad2tech in and train the model
    g2t_mod = g2t_mod_operations(g2t)

    #forth, feed the gradTech2amount in and train the model
    g2a_mod = g2a_mod_operations(g2a)

    #fifth, loading the templates from the templates folder, and print the result
    word_vec = make_context_vector(main_source, word_to_ix=None)





def g2g_mod_operations(g2g):
    data = list()
    for i in range(CONTEXT_SIZE, len(g2g) - CONTEXT_SIZE):
        data_context = list()
        for j in range(CONTEXT_SIZE):
            data_context.append(g2g[i - CONTEXT_SIZE + j])

        for j in range(1, CONTEXT_SIZE + 1):
            data_context.append(g2g[i + j])
        data_target = g2g[i]
        data.append((data_context, data_target))

    print("Some data: ", data[:3])

    unique_vocab = list(set(g2g))

    # mapping to index
    word_to_idx = {w: i for i, w in enumerate(unique_vocab)}

    # train model- changed global variable if needed
    g2g_model = grad2grad.grad2grad_model(data, unique_vocab, word_to_idx)

    # get two words similarity
    cbow_recp.get_percentage(g2g_model, unique_vocab, word_to_idx,0,0)

    return g2g_model



def g2a_mod_operations(g2a):
    data = list()
    for i in range(CONTEXT_SIZE, len(g2a) - CONTEXT_SIZE):
        data_context = list()
        for j in range(CONTEXT_SIZE):
            data_context.append(g2a[i - CONTEXT_SIZE + j])

        for j in range(1, CONTEXT_SIZE + 1):
            data_context.append(g2a[i + j])
        data_target = g2a[i]
        data.append((data_context, data_target))

    print("Some data: ", data[:3])

    unique_vocab = list(set(g2a))

    # mapping to index
    word_to_idx = {w: i for i, w in enumerate(unique_vocab)}

    # train model- changed global variable if needed
    g2a_model = gradTech2amount.GTA_model(data, unique_vocab, word_to_idx)

    # get two words similarity
    cbow_recp.get_percentage(g2a_model, unique_vocab, word_to_idx, 0, 0)

    return g2a_model

def g2t_mod_operations(g2t):
    data = list()
    for i in range(CONTEXT_SIZE, len(g2t) - CONTEXT_SIZE):
        data_context = list()
        for j in range(CONTEXT_SIZE):
            data_context.append(g2t[i - CONTEXT_SIZE + j])

        for j in range(1, CONTEXT_SIZE + 1):
            data_context.append(g2t[i + j])
        data_target = g2t[i]
        data.append((data_context, data_target))

    print("Some data: ", data[:3])

    unique_vocab = list(set(g2t))

    # mapping to index
    word_to_idx = {w: i for i, w in enumerate(unique_vocab)}

    # train model- changed global variable if needed
    g2t_model = grad2tech.grad2tech_model(data, unique_vocab, word_to_idx)

    # get two words similarity
    cbow_recp.get_percentage(g2t_model, unique_vocab, word_to_idx, 0, 0)

    return g2t_model


def make_context_vector(context, word_to_ix):
    idxs = [word_to_ix[w] for w in context]
    return torch.tensor(idxs, dtype=torch.long)

def get_max_prob_result(input, ix_to_word):
    return ix_to_word[get_index_of_max(input)]

def get_index_of_max(input):
    index = 0
    for i in range(1, len(input)):
        if input[i] > input[index]:
            index = i
    return index

"""
def get_per(model):
    context = ['People', 'create', 'to', 'direct']
    context_vector = make_context_vector(context, word_to_ix)
    a = model(context_vector).data.numpy()
    print('Raw text: {}\n'.format(' '.join(raw_text)))
    print('Context: {}\n'.format(context))
    print('Prediction: {}'.format(get_max_prob_result(a[0], ix_to_word)))

"""
if __name__ == '__main__':
    main()

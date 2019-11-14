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
EPOCH = 40
VERVOSE = 5


def set_word_ix(vocab):
    word_to_ix = {}
    ix_to_word = {}
    vocab_size = len(vocab)
    for i, word in enumerate(vocab):
        word.replace("  "," ")
        word_to_ix[word] = i
        ix_to_word[i] = word

    return word_to_ix,ix_to_word

def set_word_ix_amount(amount, grads):
    word_to_ix = {}
    ix_to_word = {}
    vocab = amount + grads
    for i, word in enumerate(vocab):
        word.replace("  "," ")
        word_to_ix[word] = i
        ix_to_word[i] = word


def main():
    ctx_size = input("Please enter the number of sources you want to use:   ") #CONTEXT_SIZE
    main_source = input("Please enter the sources you want them in the cocktail recipe, please enter them with ',' to separate:     ")

    #first, load the information from the database
    #g2g, expects combination of gradients,g2a amounts and gradients, gradient and its techniques
    (g2g, g2a, g2t) = load_cocktail_recp.grad_grad()

    #g2g outputs {recp: grad}


    #create a for loop to generate the expected number of sources in recipe.
    num_sources = len(main_source.split(","))
    context = main_source.split(",")
    tmp = ""
    for x in range(0,len(context)):
        if x != num_sources-1:
            tmp+= str(context[x]) + ","
        elif x < num_sources:
            tmp += str(context[x])

    context = tmp
    #set up unique vocabs
    uniq_grad = get_uniq(g2g)
    file = open("all_gradients.txt","w")
    for x in uniq_grad:
        file.write(x)
        file.write("\n")

    file.close()
    # uniq_amount = get_uniq(g2a[recp_name])
    # uniq_tech = get_uniq(g2t[recp_name])
    word_to_idx, ix_to_word = set_word_ix(uniq_grad)
    for num in range(num_sources, int(ctx_size)):
        # get the trained models for each model, under the context right now
        # initialize the models first
        # do modifications here
        EMBEDDING_DIM = int(300 / num)
        g2g_mod = cbow_recp.CBOW(len(uniq_grad), EMBEDDING_DIM, num)  # gta = CBOW(len(unique_vocab), EMBEDDING_DIM, CONTEXT_SIZE)
        for recp_name in g2g:
            #get_result
            g2g_mod = g2g_mod_operations(g2g[recp_name], g2g_mod, num, word_to_idx)

        pred_result = get_pred(g2g_mod, context, word_to_idx, ix_to_word)
        context += ", " + pred_result


    #now find the amount and the grad
    uniq_amount = amount_uniq(g2a)
    #context = 2

    word_to_idx_a, ix_to_word_a = set_word_ix(uniq_amount)
    word_to_idx.update(word_to_idx_a)
    ix_to_word.update(ix_to_word_a)
    g2a_mod = cbow_recp.CBOW(len(word_to_idx.items()), 300, 1)
    pred_amount = list()
    context = context.split(",")
    for x in context:
        for recp_name in g2a:
            amount = g2a[recp_name]
            g2a_mod = g2a_mod_operations(amount, g2a_mod, 2, word_to_idx)

        pred_a = get_pred(g2a_mod,x, word_to_idx, ix_to_word)
        pred_amount.append(pred_a)


    print(pred_amount)



    return context

def get_uniq(context):
    total_vocab = list()
    for x in context:
        context1 = context[x]

        context1 = context1.replace(", ",",")
        context1 = context1.replace("  "," ")
        splt_ctx = context1.split(",")
        total_vocab += splt_ctx
    return set(total_vocab)

def g2g_mod_operations(g2g, g2g_mod, size,word_to_idx):
    data = list()
    g2g = g2g.replace(", ",",")
    g2g = g2g.replace("  "," ")
    g2g = g2g.split(",")
    #print(g2g)
    #cases when there are not enough
    try:
        for i in range(size, len(g2g) - size):
            data_context = list()
            for j in range(size):
                data_context.append(g2g[i - size + j])
                print(data_context)
            for j in range(1, size + 1):
                data_context.append(g2g[i + j])
                print(data_context)
            data_target = g2g[i]
            data.append((data_context, data_target))

        if(len(g2g)-size-1) <= 0:
            for x in range(0, size-1):
                data_context.append(g2g[0+x])
            data_target.append(g2g[size])
            data.append((data_context,data_target))

        print("Some data: ", data[:3])


        # train model- changed global variable if needed
        g2g_model = grad2grad.grad2grad_model(g2g_mod, data, word_to_idx)
    except:
        g2g_model = g2g_mod


    return g2g_model

def amount_uniq(g2a):
    amount_uniq = list()
    for x in g2a:
        g2a[x] = g2a[x].replace(", ",",")
        g2a[x] = g2a[x].replace(". ",".")
        g2a[x] = g2a[x].replace("  "," ")
        individuals = g2a[x].split(",")
        for ind in individuals:
            try:
                ind = ind.split(" ")
                amount_uniq.append(ind[0] + " " + ind[1])
            except:
                pass


    return set(amount_uniq)





def g2t_mod_operations(g2t, g2t_mod, size, unique_vocab, input_ctx):
    data = g2t.split(",")
    for i in range(size, len(g2t) - size):
        data_context = list()
        for j in range(size):
            data_context.append(g2t[i - size + j])

        for j in range(1, size + 1):
            data_context.append(g2t[i + j])
        data_target = g2t[i]
        data.append((data_context, data_target))

    print("Some data: ", data[:3])

    # mapping to index
    word_to_idx, ix_to_word = set_word_ix(unique_vocab)

    # train model- changed global variable if needed
    g2g_model = grad2grad.grad2grad_model(g2t_mod, data, word_to_idx)

    pred_result = get_pred(g2g_model,input_ctx,word_to_idx, ix_to_word)

    return pred_result

def g2a_mod_operations(g2a, g2a_mod, size,word_to_idx):
    g2a = g2a.replace(", ", ",")
    g2a = g2a.replace(". ", ".")
    g2a = g2a.replace("  ", " ")
    g2a = g2a.split(",")
    data = list()
    try:
        for x in g2a:
            x = x.split(" ")
            data1 = x[:2]
            data1 = " ".join(data1)
            data2 = x[2:]
            data2 = " ".join(data2)
            data_context = list()
            data_context.append(data1)
            data_context.append(data2)


            data.append((data_context, data1))

        print("Some data: ", data[:3])

    # train model- changed global variable if needed
        g2a_model = grad2grad.grad2grad_model(g2a_mod, data, word_to_idx)
    except Exception as e:
        g2a_model = g2a_mod

    return g2a_model


def make_context_vector(context, word_to_ix):
    context = context.split(", ")
    context = list(context)
    idxs = [word_to_ix[w.strip()] for w in context]
    return torch.tensor(idxs, dtype=torch.long)

def get_max_prob_result(input, ix_to_word):
    return ix_to_word[get_index_of_max(input)]

def get_index_of_max(input):
    index = 0
    for i in range(1, len(input)):
        if input[i] > input[index]:
            index = i
    return index

#takes the input sources, generate one that is most likely to be "successful"
def get_pred(model, context, word_to_ix, ix_to_word):
    context_vector = make_context_vector(context, word_to_ix)
    a = model(context_vector).data.numpy()
    predicted_source = get_max_prob_result(a[0], ix_to_word)
    print('Prediction: {}'.format(get_max_prob_result(a[0], ix_to_word)))
    return predicted_source


if __name__ == '__main__':
    print(main())

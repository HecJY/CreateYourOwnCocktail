import back_end.grad2grad as grad2grad
import back_end.load_cocktail_recp as load_cocktail_recp
import back_end.cbow_recp as cbow_recp
import torch
import re

VERVOSE = 5



def set_actions(vocab):
    word_to_ix = {}
    for i, word in enumerate(vocab):
        word.replace("  "," ")
        word_to_ix[word] = 0

    return word_to_ix
def set_word_ix(vocab):
    word_to_ix = {}
    ix_to_word = {}
    vocab_size = len(vocab)
    for i, word in enumerate(vocab):
        word.replace("  "," ")
        word_to_ix[word] = i
        ix_to_word[i] = word

    return word_to_ix,ix_to_word



def back_end(ctx_size, main_source, g2g, g2a, g2t):
    #create a for loop to generate the expected number of sources in recipe.
    num_sources = len(main_source.split(","))
    context = main_source.split(",")
    ctx = context
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
        emb = 300
        g2g_mod = cbow_recp.CBOW(len(uniq_grad), emb, num)  # gta = CBOW(len(unique_vocab), EMBEDDING_DIM, CONTEXT_SIZE)
        for recp_name in g2g:
            #get_result
            g2g_mod = g2g_mod_operations(g2g[recp_name], g2g_mod, num, word_to_idx)

        pred_result = get_pred(g2g_mod, context, word_to_idx, ix_to_word)
        context += ", " + pred_result

    final = context.split(", ")
    recp_total = list()
    amount = list()
    for x in final:
        ind_a = list()
        recp_ind = list()
        for y in g2a:
            g2g[y] = g2g[y].replace("  "," ")
            g2g[y] = g2g[y].replace(", ", ",")
            g2g[y] = g2g[y].replace(". ", ".")
            g2g[y] = g2g[y].replace(" . ", ".")


            if x in g2a[y]:
                recp_ind.append(y)
                spt = g2a[y].split(", ")
                for z in spt:
                    z = z.replace("  ", " ")
                    z = z.replace(", ", ",")
                    z = z.replace(". ", ".")
                    z = z.replace(" . ", ".")
                    if x in z:
                        z = z.split(" ")
                        amt = z[:2]
                        amt = " ".join(amt)
                        if re.findall(r"[0-9]",amt):
                            ind_a.append(amt)
        amount.append(ind_a)
        recp_total.append(recp_ind)

    cock_action = dict()
    actions = load_cocktail_recp.actions()

    index = 0
    for x in recp_total:
        action_to_id = set_actions(actions)
        for y in x:
            for a in actions:
                if a.lower() in g2t[y].lower():
                    action_to_id[a] += 1

        cock_action[final[index]] = action_to_id
        index += 1




    return final, amount, cock_action




def main():
    ctx_size = input("Please enter the number of sources you want to use:   ") #CONTEXT_SIZE
    main_source = input("Please enter the sources you want them in the cocktail recipe, please enter them with ',' to separate:     ")

    #first, load the information from the database
    #g2g, expects combination of gradients,g2a amounts and gradients, gradient and its techniques
    (g2g, g2a, g2t) = load_cocktail_recp.grad_grad()


    #create a for loop to generate the expected number of sources in recipe.
    num_sources = len(main_source.split(","))
    context = main_source.split(",")
    ctx = context
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
        EMBEDDING_DIM = 300
        g2g_mod = cbow_recp.CBOW(len(uniq_grad), EMBEDDING_DIM, num)  # gta = CBOW(len(unique_vocab), EMBEDDING_DIM, CONTEXT_SIZE)
        for recp_name in g2g:
            #get_result
            g2g_mod = g2g_mod_operations(g2g[recp_name], g2g_mod, num, word_to_idx)

        pred_result = get_pred(g2g_mod, context, word_to_idx, ix_to_word)
        print(pred_result)
        context += ", " + pred_result

    final = context.split(", ")
    recp_total = list()
    amount = list()
    for x in final:
        ind_a = list()
        recp_ind = list()
        for y in g2a:
            g2g[y] = g2g[y].replace("  "," ")
            g2g[y] = g2g[y].replace(", ", ",")
            g2g[y] = g2g[y].replace(". ", ".")
            g2g[y] = g2g[y].replace(" . ", ".")


            if x in g2a[y]:
                recp_ind.append(y)
                spt = g2a[y].split(", ")
                for z in spt:
                    z = z.replace("  ", " ")
                    z = z.replace(", ", ",")
                    z = z.replace(". ", ".")
                    z = z.replace(" . ", ".")
                    if x in z:
                        z = z.split(" ")
                        amt = z[:2]
                        amt = " ".join(amt)
                        if re.findall(r"[0-9]",amt):
                            ind_a.append(amt)
        amount.append(ind_a)
        recp_total.append(recp_ind)

    cock_action = dict()
    actions = load_cocktail_recp.actions()

    index = 0
    for x in recp_total:
        action_to_id = set_actions(actions)
        for y in x:
            for a in actions:
                if a.lower() in g2t[y].lower():
                    action_to_id[a] += 1

        cock_action[final[index]] = action_to_id
        index += 1





    print(amount)
    print(final)

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
            data_context = list()
            data_target = list()
            for x in range(0, size-1):
                data_context.append(g2g[0+x])
                data_target.append(g2g[size])
            data.append((data_context,data_target))

        print("Some data: ", data[:3])


        # train model- changed global variable if needed
        g2g_model = grad2grad.grad2grad_model(g2g_mod, data, word_to_idx)
    except Exception as e:
        print(e)
        g2g_model = g2g_mod


    return g2g_model




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

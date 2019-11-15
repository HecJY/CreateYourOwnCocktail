from back_end.cbow_recp import *
from back_end.load_cocktail_recp import *

def grad2grad_model(ggm, data, word_to_idx):

    nll_loss = nn.NLLLoss()  # loss function
    optimizer = SGD(ggm.parameters(), lr=0.001)

    print(len(data))

    for epoch in range(40):
        total_loss = 0
        for context, target in data:
            inp_var = make_context_vector(context, word_to_idx)
            target_var = Variable(torch.LongTensor([word_to_idx[target]]))

            ggm.zero_grad()
            log_prob = ggm(inp_var)
            loss = nll_loss(log_prob, target_var)
            loss.backward()
            optimizer.step()
            total_loss += loss.data

        if epoch % 5 == 0:
            loss_avg = float(total_loss / len(data))
            print("{}/{} loss {:.2f}".format(epoch, 20, loss_avg))
    return ggm

def make_context_vector(context, word_to_ix):
    #context = context.split(", ")
    #context = list(context)
    idxs = [word_to_ix[w.strip()] for w in context]
    return torch.tensor(idxs, dtype=torch.long)


from cbow_recp import *
from load_cocktail_recp import *

def grad2grad_model(data, unique_vocab, word_to_idx):
    ggm = CBOW(len(unique_vocab), EMBEDDING_DIM, CONTEXT_SIZE)

    nll_loss = nn.NLLLoss()  # loss function
    optimizer = SGD(ggm.parameters(), lr=0.001)

    print(len(data))

    for epoch in range(EPOCH):
        total_loss = 0
        for context, target in data:
            inp_var = Variable(torch.LongTensor([word_to_idx[word] for word in context]))
            target_var = Variable(torch.LongTensor([word_to_idx[target]]))

            ggm.zero_grad()
            log_prob = ggm(inp_var)
            loss = nll_loss(log_prob, target_var)
            loss.backward()
            optimizer.step()
            total_loss += loss.data

        if epoch % VERVOSE == 0:
            loss_avg = float(total_loss / len(data))
            print("{}/{} loss {:.2f}".format(epoch, EPOCH, loss_avg))
    return ggm



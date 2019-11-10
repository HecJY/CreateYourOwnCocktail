from cbow_recp import *
from load_cocktail_recp import *

def grad2tech_model(data, unique_vocab, word_to_idx):
    gte = CBOW(len(unique_vocab), EMBEDDING_DIM, CONTEXT_SIZE)

    nll_loss = nn.NLLLoss()  # loss function
    optimizer = SGD(gte.parameters(), lr=0.001)

    print(len(data))

    for epoch in range(EPOCH):
        total_loss = 0
        for context, target in data:
            inp_var = Variable(torch.LongTensor([word_to_idx[word] for word in context]))
            target_var = Variable(torch.LongTensor([word_to_idx[target]]))

            gte.zero_grad()
            log_prob = gte(inp_var)
            loss = nll_loss(log_prob, target_var)
            loss.backward()
            optimizer.step()
            total_loss += loss.data

        if epoch % VERVOSE == 0:
            loss_avg = float(total_loss / len(data))
            print("{}/{} loss {:.2f}".format(epoch, EPOCH, loss_avg))
    return gte


def main():
    # content processed as context/target
    # consider 2*CONTEXT_SIZE as context window where middle word as target
    data = list()
    for i in range(CONTEXT_SIZE, len(corpus_text) - CONTEXT_SIZE):
        data_context = list()
        for j in range(CONTEXT_SIZE):
            data_context.append(corpus_text[i - CONTEXT_SIZE + j])

        for j in range(1, CONTEXT_SIZE + 1):
            data_context.append(corpus_text[i + j])
        data_target = corpus_text[i]
        data.append((data_context, data_target))

    print("Some data: ", data[:3])

    unique_vocab = list(set(corpus_text))

    # mapping to index
    word_to_idx = {w: i for i, w in enumerate(unique_vocab)}

    # train model- changed global variable if needed
    cbow = train_cbow(data, unique_vocab, word_to_idx)

    # get two words similarity
    test_cbow(cbow, unique_vocab, word_to_idx)
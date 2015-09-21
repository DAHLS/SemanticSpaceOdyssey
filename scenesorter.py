import string
import numpy as np

""" FUNCTIONS """
# Word vectors generation
def word2vecindexing(sentences):
    model2001 = open("model2001").readlines()[2:]
    word2vecindex = dict()
    vecsize = len(model2001[0].split()) - 1
    for v in model2001:
        vec = v.split()
        token = vec.pop(0)
        word2vecindex[token] = [float(e) for e in vec]
    return word2vecindex, vecsize

def randomindexing(sentences, vecsize):
    tokens = gettokens(sentences)
    randomindex = dict()
    for t in tokens:
        randomindex[t] = np.random.randn(vecsize)
    return randomindex

# Helper function for random indexing, return set of unique words
def gettokens(sentences):
    terms = []
    for s in sentences:
        words = s.split()
        for w in words:
            terms.append(w)
    return set(terms)

# Constructs document vectors by adding word vectors up
# current options are random indexing and Googles word2vec model
def builddocumentvectors(sentences, vecsize=100, indexing="rand"):
    if indexing == "rand":
        randomindex = randomindexing(sentences, vecsize)
    elif indexing == "word2vec":
        randomindex, vecsize = word2vecindexing(sentences)
    else:
        raise ValueError("Incorrect indexing model chosen!")
    documentvectors = []
    for s in sentences:
        sentvec = np.zeros(vecsize)
        sent = s.split()
        for w in sent:
            sentvec += randomindex[w]
        documentvectors.append(sentvec)
    return(documentvectors)

# Assigns a single semantic score per document; two options
def centrality(documentvectors, state="closeness"):
    centralitydict = dict()
    for i, d in enumerate(documentvectors):
        similarityscores = []
        for s in documentvectors:
            similarityscores.append(cosine(d, s))
            if state == "closeness":
                centralitydict[i] = 1 / sum(similarityscores)
            elif state == "hamonic": # A variant of closeness
                centralitydict[i] = sum(map(lambda x: 1/x, similarityscores))
            else:
                raise ValueError("Incorrect centrality state chosen!")
    return centralitydict

# Similarity messure; cosine distance
def cosine(u, v):
    return  np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

# Sort timestamp and sentence lists by semantic scores.
def sorter(timecodes, sentences, similarityscores):
    timesort, sentsort = [], []
    ordertupl = sorted(similarityscores.items(), key=lambda x: x[1])
    for t in ordertupl:
        timesort.append(timecodes[t[0]])
        sentsort.append(sentences[t[0]])
    return timesort, sentsort

""" RUNTIME """
def main():
    # Initial variables
    srt = open("2001.A.Space.Odyssey.1968.720p.HDDVD.x264-hV.srt").readlines()
    punct = string.punctuation
    times = srt[0::4]
    sents = [''.join(char for char in sentstring 
                        if char not in punct).strip().lower() 
                    for sentstring in srt[2::4]]

    # Doing all the work; remember to set the state and indexing
    documentvectors = builddocumentvectors(sents, indexing='word2vec')
    simscores = centrality(documentvectors, state='closeness')
    s_times, s_sents = sorter(times, sents, simscores)

    # Output data
    for i in range(len(s_sents)):
        print(s_times[i], s_sents[i])

main()

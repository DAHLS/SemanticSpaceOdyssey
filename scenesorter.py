import string
import numpy as np

def gettokens(sentences):
    terms = []
    for s in sentences:
        words = s.split()
        for w in words:
            terms.append(w)
    return set(terms)

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

def builddocumentvectors(sentences, vecsize=100, indexing="rand"):
    if indexing == "rand":
        randomindex = randomindexing(sentences, vecsize)
    elif indexing == "word2vec":
        randomindex, vecsize = word2vecindexing(sentences)
    documentvectors = []
    for s in sentences:
        sentvec = np.zeros(vecsize)
        sent = s.split()
        for w in sent:
            sentvec += randomindex[w]
        documentvectors.append(sentvec)
    return(documentvectors)

def closenesscentrality(documentvectors):
    closenessindexdict = dict()
    for i, d in enumerate(documentvectors):
        similarityscores = []
        for s in documentvectors:
            similarityscores.append(cosine(d, s))
        closenessindexdict[i] = 1 / sum(similarityscores)
    return closenessindexdict

def cosine(u, v):
    return  np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def sorter(timecodes, sentences, similarityscores):
    timesort, sentsort = [], []
    ordertupl = sorted(similarityscores.items(), key=lambda x: x[1])
    for t in ordertupl:
        timesort.append(timecodes[t[0]])
        sentsort.append(sentences[t[0]])
    return timesort, sentsort

srt = open("2001.A.Space.Odyssey.1968.720p.HDDVD.x264-hV.srt").readlines()
punct = string.punctuation
times = srt[0::4]
sents = [''.join(char for char in sentstring 
                      if char not in punct).strip().lower() 
                 for sentstring in srt[2::4]]

documentvectors = builddocumentvectors(sents, indexing='word2vec')
simscores = closenesscentrality(documentvectors)
s_times, s_sents = sorter(times, sents, simscores)

for i in range(len(s_sents)):
    print(s_times[i], s_sents[i])

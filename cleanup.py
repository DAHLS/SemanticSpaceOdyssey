srt = open("2001.A.Space.Odyssey.1968.720p.HDDVD.x264-hV.srt").readlines()
sents = srt[2:10:4]
punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
cleansents = [''.join(char for char in sentstring if char not in punct).strip().lower() for sentstring in sents]
with open("2001sents.txt", "w") as f:
    for i in cleansents:
        f.write("%s\n" % i)
    f.close()

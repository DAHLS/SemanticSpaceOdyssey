punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

def subcleanup():
    srt = open("2001.A.Space.Odyssey.1968.720p.HDDVD.x264-hV.srt").readlines()
    sents = srt[2:10:4]
    cleansents = [''.join(char for char in sentstring if char not in punct).strip().lower() for sentstring in sents]
    with open("2001sents.txt", "w") as f:
        for i in cleansents:
            f.write("%s\n" % i)
        f.close()

def scriptclean()
    script = open("data/Script___2001___A_Space_Odyssey.txt").read().lower().split()

srt = open("2001.A.Space.Odyssey.1968.720p.HDDVD.x264-hV.srt").readlines()
times = srt[0::4]

print(times[0:10])

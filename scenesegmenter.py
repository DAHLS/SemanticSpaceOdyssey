import sys
import subprocess as subp

videoPath = sys.argv[1]
#ffmpeg does not work properly right now
ffmpegCommand = "ffmpeg -i {} -vcodec copy -acodec copy -ss {} -to {} data/movie_segments/{}"
srt = open("data/2001.A.Space.Odyssey.1968.720p.HDDVD.x264-hV.srt").readlines()
times = [(t.split()[0], t.split()[2]) for t in srt[1::4]]


def incrementtime(timeStamp, extraTime=500): 
    intTime = int(''.join([i for i in timeStamp if i.isdigit()]))
    intTime += extraTime #extraTime is in hundreds of seconds
    if int(timeStamp[1]) == 0:
        zeroZero = "00"
    else:
        zeroZero = "0"
    newStamp = zeroZero + str(intTime)[:2] + str(intTime)[2:4] + \
               str(intTime)[4:6] + str(intTime)[6:]
    newStamp = newStamp[:2] + ':' + newStamp[2:4] + ':' + \
               newStamp[4:6] + '.' + newStamp[6:]
    return newStamp

def cutsegments(timeStamps, videoPath, command):
     for i, t in enumerate(timeStamps):
         startTimeZero, startTimeOne = t[0].split(',')
         startTime = startTimeZero + '.' + startTimeOne
         endTime = incrementtime(t[-1])
         segment = subp.Popen(command.format(videoPath, startTime, \
                              endTime, "out"+str(i)+".mp4").split(), \
                              stderr=subp.PIPE, stdout=subp.PIPE)
         segment.communicate()

cutsegments(times, videoPath, ffmpegCommand)

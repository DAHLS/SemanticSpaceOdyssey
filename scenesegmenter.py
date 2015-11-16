import sys
import subprocess as subp
from glob import glob

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

def cutsegments(timeStamps, videoPath, command, completedSegments):
     for i, t in enumerate(timeStamps):
         segmentName = "data/movie_segments/out" + str(i) + ".mp4"
         if segmentName in completedSegments:
             pass
         else:
            startTimeZero, startTimeOne = t[0].split(',')
            startTime = startTimeZero + '.' + startTimeOne
            endTime = incrementtime(t[-1])
            print("Processing " + segmentName.split('/')[-1], end="; ")
            segment = subp.Popen(command.format(videoPath, startTime, \
                                endTime, segmentName).split(), \
                                stderr=subp.PIPE, stdout=subp.PIPE)
            _, err = segment.communicate()
            if err:
                print("FAILED")
            else:
                segment.wait()
                print("DONE")

def main():
    priorSegmentPaths = glob("data/movie_segments/*")
    movPaths = ("data/2001.A.Space.Odyssey.1968.720p.BrRip.x264.YIFY.mp4",
                "data/2001.A.Space.Odyssey.1968.720p.HDDVD.x264-hV.srt")

    ffmpegCommand = "ffmpeg -i {} -ss {} -to {} -c:v libx264 -preset veryslow -qp 10 -acodec copy {}"
    videoPath = movPaths[0]
    srt = open(movPaths[1]).readlines()
    times = [(t.split()[0], t.split()[2]) for t in srt[1::4]]

    cutsegments(times, videoPath, ffmpegCommand, priorSegmentPaths)

main()

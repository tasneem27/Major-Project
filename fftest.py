import subprocess

#command = "ffmpeg -i C:/trump.mp4 -ab 160k -ac 2 -ar 44100 -vn audiotru.raw"

#command ="ffmpeg -i C:/sushma.mp4 "

#command= "ffmpeg -i C:\sushma.mp4 -map 0:s:0 C:\sub.srt"

command="ffmpeg -i C:/clear.mp4 -acodec pcm_s16le -ac 1 -ar 16000 clear.wav"


subprocess.call(command, shell=True)

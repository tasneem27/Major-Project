
import argparse
import fileinput
import re
import subprocess
import sys

subnum = 1
words = []
inSentence = False
def processLine(line):
	global subnum, words, inSentence
	
	bits = line.split(' ')
	
	if bits[0] == '<s>':
		inSentence = True
	else:
		if not inSentence:
			return
		
		if bits[0] == '</s>':
			i = 0
			while i < len(words):
				subtitle = None
				if len(words) - i + 1 < 14: # If fewer than 14 words remaining, put them on one line
					subtitle = words[i:]
					i = len(words)
				else:
					subtitle = words[i:i+10]
					i += 10
				
				output.write('{}\n'.format(subnum))
				output.write('{} --> {}\n'.format(secondsToTime(subtitle[0]['startTime']), secondsToTime(subtitle[-1]['endTime'])))
				output.write('{}\n'.format(joinWords(subtitle)))
				output.write('\n')
				
				subnum += 1
			del words[:]
			#words.clear()
			inSentence = False
		else:
			if bits[0][0] != '<' and bits[0][0] != '[':
                                #words.append({'text': re.sub('\(.*?\)', '', bits[0])})
                                #print "%c %c" %(bits[1], bits[2])

				words.append({'text': re.sub('\(.*?\)', '', bits[0]), 'startTime': bits[1], 'endTime': bits[2]})
	
	output.flush()

def secondsToTime(sec):
	sec = float(sec)
	hours = int(sec // 3600)
	minutes = int((sec % 3600) // 60)
	seconds = int((sec % 60) // 1)
	msecs = int((sec % 1) // 0.001)
	return '{:}:{:02}:{:02},{:03}'.format(hours, minutes, seconds, msecs)

def joinWords(words):
	text = '';
	for word in words:
		if text != '':
			text += ' '
		text += word['text']
	return text

parser = argparse.ArgumentParser(description='Generate a transcript from an audio file using pocketsphinx.')
parser.add_argument('--inputwav', '-i', metavar='FILE', help='16kHz 16-bit mono audio file')
parser.add_argument('--inputtext', '-t', metavar='FILE', help='filename containing previously computed pocketsphinx (-time yes) output')
parser.add_argument('--output', '-o', metavar='FILE', help='filename to save srt output to')
parser.add_argument('args', help='arguments to pass to pocketsphinx', nargs=argparse.REMAINDER)

args = parser.parse_args()

if '--' in args.args:
	args.args.remove('--')

output = sys.stdout

if args.output and args.output != '-':
	output = open(args.output, 'w')

if args.inputwav:
	sphinxargs = ['C:\\Python27\\Lib\\site-packages\\pocketsphinx\\bin\\Release\\Win32\\pocketsphinx_continuous', '-infile', args.inputwav, '-time', 'yes']
	sphinxargs.extend(args.args)
	proc = subprocess.Popen(sphinxargs, stdout=subprocess.PIPE, universal_newlines=True,shell=True)
	for line in proc.stdout:
		processLine(line)
elif args.inputtext:
	for line in fileinput.input(args.inputtext):
		processLine(line)

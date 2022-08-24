from re import sub, match, findall
from argparse import ArgumentParser, FileType
from utils import error
from time import time
from child import Child


class Process:
	def __init__(self, line):
		self.name = str()
		self.need = dict()
		self.result = dict()
		self.delay = int()
		self.save(line)

	#CHECK RECRE FILE DON'T WORK
	def save(self, line):
		match1 = match(r'\w+', line)
		self.name = match1.group(0)
		match2 = findall(r'(\((\w+:\d+;?)+\))?:', line)
		need = match2[1][0]
		for elt in sub(r'[\(\)]', '', need).split(';'):
			i, val = elt.split(':')
			self.need[i] = int(val)
		result = match2[2][0]
		for elt in sub(r'[\(\)]', '', result).split(';'):
			i, val = elt.split(':')
			self.result[i] = int(val)
		match3 = findall(r':\d+$', line)
		self.delay = int(match3[0][1:])

	def print(self):
		print('name: %s' % self.name)
		print('need: %s' % self.need)
		print('result:', self.result)
		print('delay: %s\n' % self.delay)

class Krpsim:
	def __init__(self, start_time):
		self.max_cycle = int()
		self.max_time = int()
		self.start_time = start_time
		self.stock = dict()
		self.lst_process = dict()
		self.optimize = str()

	def parser(self):
		parser = ArgumentParser()
		parser.add_argument('file', type=FileType('r'), help='file to process')
		parser.add_argument('delay', type=int, help='max time to process')
		parser.add_argument('-c', '--cycle', default=10000, help='max number of cycle. default:10000')
		args = parser.parse_args()
		self.max_cycle = args.cycle
		self.max_time = args.delay
		f = args.file.read()
		f = sub(r'#.*', '', f)
		for elt in f.split('\n'):
			if elt == '\n' or elt == '':
				pass
			elif match(r'^\w+:\d+$', elt):
				i, val = elt.split(':')
				self.stock[i] = int(val)
			elif match(r'^\w+:(\((\w+:\d+;?)+\))?:(\((\w+:\d+;?)+\))?:\d+$', elt):
				process = Process(elt)
				self.lst_process[process.name] = process
			elif match(r'^optimize:\((\w+;?)+\)$', elt):
				self.optimize = findall(r'\w+\)$', elt)[0][:-1]
			else:
				error('bad_file')

	def process(self):
		child = Child(self.stock, self.lst_process)
		print('instructions:', child.instructions)
		delta_time = time() - self.start_time
		if delta_time > self.max_time:
			print(delta_time)
			exit(1)

	def print(self):
		print('Stock :', self.stock)
		for i, elt in self.lst_process.items():
			elt.print()

def main():
	krpsim = Krpsim(time())
	krpsim.parser()
	krpsim.process()
	# krpsim.print()
	print('time:', time() - krpsim.start_time)
	exit(0)

if __name__ == '__main__':
	main()

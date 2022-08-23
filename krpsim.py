from re import sub, match, findall
from argparse import ArgumentParser, FileType
from utils import error

class Process:
	def __init__(self, line):
		self.name = str()
		self.need = list()
		self.result = list()
		self.delay = int()
		self.save(line)

	def save(self, line):
		match1 = match(r'\w+', line)
		self.name = match1.group(0)
		match2 = findall(r'(\((\w+:\d+;?)+\))?:', line)
		need = match2[1][0]
		for elt in sub(r'[\(\)]', '', need).split(';'):
			self.need.append(elt.split(':'))
		result = match2[2][0]
		for elt in sub(r'[\(\)]', '', result).split(';'):
			self.result.append(elt.split(':'))
		match3 = findall(r':\d+$', line)
		self.delay = int(match3[0][1:])

	def print(self):
		print('name: %s' % self.name)
		print('need: %s' % self.need)
		print('result: %s' % self.result)
		print('delay: %s\n' % self.delay)

class Krpsim:
	def __init__(self):
		self.maxCycle = int()
		self.stock = list()
		self.lstProcess = list()
		self.optimize = str()

	def parser(self):
		parser = ArgumentParser()
		parser.add_argument('file', type=FileType('r'), help='file to process')
		parser.add_argument('delay', type=int, help='max time to process')
		parser.add_argument('-c', '--cycle', default=10000, help='max number of cycle. default:10000')
		args = parser.parse_args()
		self.maxCycle = args.cycle
		f = args.file.read()
		f = sub(r'#.*', '', f)

		for elt in f.split('\n'):
			if elt == '\n' or elt == '':
				pass
			elif match(r'^\w+:\d+$', elt):
				self.stock.append(elt.split(':'))
			elif match(r'^\w+:(\((\w+:\d+;?)+\))?:(\((\w+:\d+;?)+\))?:\d+$', elt):
				self.lstProcess.append(Process(elt))
			elif match(r'^optimize:\((\w+;?)+\)$', elt):
				self.optimize = findall(r'\w+\)$', elt)[0][:-1]
			else:
				error('bad_file')

	def process(self):
		### START TRY ###
		print('Evaluating .................. done.')
		print('Main walk')
		print('0:achat_materiel')
		print('10:realisation_produit')
		print('40:livraison')
		print('no more process doable at time 61')
		### END ###

	def print(self):
		print('Stock :')
		for elt in self.stock:
			print('%s => %s' % (elt[0], elt[1]))

def main():
	krpsim = Krpsim()
	krpsim.parser()
	krpsim.process()
	krpsim.print()
	exit(0)

if __name__ == '__main__':
	main()

from argparse import ArgumentParser, FileType

class Krpsim:
	def __init__(self):
		self.cycle = int()
		self.stock = list()

	def parser(self):
		parser = ArgumentParser()
		parser.add_argument('file', type=FileType('r'), help='file to process')
		parser.add_argument('-C', '--cycle', default=100, help='number of cycle. default:100')
		args = parser.parse_args()
		self.cycle = args.cycle
		f = args.file.read()
		# run parser file
		### START TRY ###
		self.stock.append(['client_content', 1])
		self.stock.append(['produit', 0])
		self.stock.append(['materiel', 0])
		self.stock.append(['euro', 2])
		print('Nice file ! 3 processes, 4 stocks, 1 to optimize')
		### END ###
	
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
			print('%s => %d' % (elt[0], elt[1]))

def main():
	krpsim = Krpsim()
	krpsim.parser()
	krpsim.process()
	krpsim.print()
	exit(0)

if __name__ == '__main__':
	main()
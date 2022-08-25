from random import choice

class Child:
	def __init__(self, start_stock, lst_process, optimize):
		self.has_stock = start_stock
		self.need_stock = dict()
		self.instructions = list()
		self.score = int()
		self.opt_val = int()
		self.optimize = optimize
		self.genInstructions(lst_process)

	def genInstructions(self, lst_process):
		self.selectNeedProcess(lst_process)#init besoin et instructions
		print('END', self.instructions, self.need_stock)
		exit(0)
		while self.need_stock:
			pass#remplir 1 besoin

	def selectNeedProcess(self, lst_process):
		lst_possible_process = self.listPossibleProcess(lst_process, self.optimize)
		chosen_process = choice(lst_possible_process)
		self.instructions.append(chosen_process.name)
		self.updateAddNeedStock(chosen_process.need)

	def updateAddNeedStock(self, items):
		for elt in items:
			try:
				self.need_stock[elt] += items[elt]
			except KeyError:
				self.need_stock[elt] = items[elt]

	def updateDelNeedStock(self, items): #normalement pas de try except mais pour l'instant flemme de verif
		for key, value in items:
			try:
				self.need_stock[key] -= value
			except KeyError:
				self.need_stock[key] = -value

	def listPossibleProcess(self, lst_process, need_name): # need_quantity: unsigned int zith -1 for start (tranfromed into max uint=2*217183647 + 1)
		lst_possible_process = list()
		for process in lst_process:
			if need_name in lst_process[process].result.keys():
				lst_possible_process.append(lst_process[process])
		return lst_possible_process

# 	def remplirBesoin(self):
# 		#choisir aleatoirement quel process pour remplir besoin
# 		#update need_stock (retirer cause de la fonction, ajouter cout)
# 		#ajouter process a liste d'instructions
# 		#si pas possible de remplir le besoin, l'enfant est con et moche donc stop
# 		pass

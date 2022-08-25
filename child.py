from pickletools import optimize
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
		self.selectProcess(self.optimize, 10000, lst_process)#init besoin et instructions
		while self.need_stock != {}:
			#remplir 1 besoin
			print(self.instructions, self.need_stock)
			name1 = list(self.need_stock.keys())[0]
			self.selectProcess(name1, self.need_stock[name1], lst_process)

	def selectProcess(self, need_name, need_quantity, lst_process):
		lst_possible_process = self.listPossibleProcess(need_name, lst_process)
		chosen_process = choice(lst_possible_process)
		if chosen_process.name == 'take_from_stock': #that not a struct, need to find something
			nb = self.has_stock[need_name] - need_quantity
			if nb < 0:
				self.has_stock[need_name] = 0
				self.updateSubNeedStock({need_name: nb})
			else:
				self.has_stock[need_name] = nb
				del self.need_stock[need_name]
		else:
			self.instructions.append(chosen_process.name) #ici frero
			self.updateAddNeedStock(chosen_process.need)
			self.updateSubNeedStock(chosen_process.result)

	# def updateHasStock(self, need_name, need_quantity):


	def updateAddNeedStock(self, items):
		for elt in items:
			try:
				self.need_stock[elt] += items[elt]
			except KeyError:
				self.need_stock[elt] = items[elt]

	def updateSubNeedStock(self, items): #normalement pas de try except mais pour l'instant flemme de verif
		for elt in items:
			try:
				self.need_stock[elt] -= items[elt]
			except KeyError:
				self.need_stock[elt] = -items[elt]
			if self.need_stock[elt] <= 0:
				del self.need_stock[elt]

	def listPossibleProcess(self, need_name, lst_process): # need_quantity: unsigned int zith -1 for start (tranfromed into max uint=2*217183647 + 1)
		lst_possible_process = list()
		for process in lst_process:
			if need_name in lst_process[process].result.keys():
				lst_possible_process.append(lst_process[process])
		if need_name in list(self.has_stock.keys()):
			lst_possible_process.append({'name': 'take_from_stock'})
			print('lst_possible_process:', lst_possible_process[0].name)
		return lst_possible_process

# 	def remplirBesoin(self):
# 		#choisir aleatoirement quel process pour remplir besoin
# 		#update need_stock (retirer cause de la fonction, ajouter cout)
# 		#ajouter process a liste d'instructions
# 		#si pas possible de remplir le besoin, l'enfant est con et moche donc stop
# 		pass

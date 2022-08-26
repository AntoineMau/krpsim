from random import choice
from math import ceil

class Child:
	def __init__(self, start_stock, lst_process, optimize):
		self.has_stock = start_stock.copy()
		self.need_stock = dict()
		self.instructions = list()
		self.score = int()
		self.opt_val = int()
		self.optimize = optimize
		self.genInstructions(lst_process)

	def genInstructions(self, lst_process):
		self.selectProcess(self.optimize, -1, lst_process)#init besoin et instructions
		while self.need_stock != {}:
			print(self.need_stock)
			name1 = list(self.need_stock.keys())[0]
			if not self.selectProcess(name1, self.need_stock[name1], lst_process):
				print('Enfant con et moche donc stop')
				break
		# print('self.has_stock:', self.has_stock)

	def selectProcess(self, need_name, need_quantity, lst_process):
		if (need_name in list(self.has_stock.keys())) and need_quantity != -1:
			nb = self.has_stock[need_name] - need_quantity
			if nb < 0:
				del self.has_stock[need_name]
				self.updateSubNeedStock({need_name: nb})
			else:
				self.has_stock[need_name] = nb
				# print(self.need_stock)
				del self.need_stock[need_name]
		else:
			lst_possible_process = self.listPossibleProcess(need_name, lst_process)
			if not lst_possible_process:
				return False
			chosen_process = choice(lst_possible_process)
			self.appendProcess(need_name, need_quantity, chosen_process)
			#print('chosen_process.need:', chosen_process.need)
			#print('self.need_stock:', self.need_stock)
		return True

	def appendProcess(self, need_name, need_quantity, chosen_process):
		nb = 1 if need_quantity == -1 else ceil(need_quantity / chosen_process.result[need_name])
		for i in range(nb):
			# print('nb:', nb, i)
			self.instructions.append(chosen_process.name)
			self.updateSubNeedStock(chosen_process.result)
			self.updateAddNeedStock(chosen_process.need)
		# if need_quantity == -1:
		# 	print('ici:',self.instructions)

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
		# if need_name in list(self.has_stock.keys()):
		# 	lst_possible_process.append({'name': 'take_from_stock'})
		# 	print('lst_possible_process:', lst_possible_process[0].name)
		return lst_possible_process

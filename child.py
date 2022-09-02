from random import choice


# Create one individual, i.e. a chain of processes that completes the creation of one or more stock to optimize
# the algorithm goes from the finished product (optimize) to list every need
class Child:
	def __init__(self, start_stock, optimize, lst_process):
		self.has_stock = start_stock.copy()
		self.need_stock = dict()
		self.instructions = list()
		self.optimize = optimize
		self.opt_val = int()  # to do, c'est quoi ?
		self.score = int()  # to do, ici ou au dessus apres tri des processes ?
		self.get_instructions(lst_process)

	# list all the processes necessary to create one or more "optimize" stock
	def get_instructions(self, lst_process):
		self.select_process(self.optimize, -1, lst_process)  # initialize need_stock with stock to optimize before while loop
		while self.need_stock != {}:
			# print(self.instructions, self.need_stock)
			need_name = list(self.need_stock.keys())[0]
			if not self.select_process(need_name, self.need_stock[need_name], lst_process):
				print('Enfant con!')  # ne pas oublier de supprimer
				break
		# print(self.instructions, self.need_stock)

	# select one of the available processes to fulfill one need
	def select_process(self, need_name, need_quantity, lst_process):
		if (need_name in list(self.has_stock.keys())) and need_quantity != -1:
			nb = self.has_stock[need_name] - need_quantity
			if nb < 0:
				del self.has_stock[need_name]
				self.update_sub_need_stock({need_name: nb})
			else:
				self.has_stock[need_name] = nb
				# print(self.need_stock)
				del self.need_stock[need_name]
		else:
			lst_possible_process = self.list_possible_process(need_name, lst_process)
			if not lst_possible_process:
				return False
			chosen_process = choice(lst_possible_process)
			self.instructions.append(chosen_process.name)
			# print('chosen_process.need:', chosen_process.need)
			# print('self.need_stock:', self.need_stock)
			self.update_sub_need_stock(chosen_process.result)
			self.update_add_need_stock(chosen_process.need)
		return True

	# list available processes to fulfill the current need
	def list_possible_process(self, need_name, lst_process):
		lst_possible_process = list()
		for process in lst_process:
			if need_name in lst_process[process].result.keys():
				lst_possible_process.append(lst_process[process])
		return lst_possible_process

	def update_add_need_stock(self, items):
		for elt in items:
			try:
				self.need_stock[elt] += items[elt]
			except KeyError:
				self.need_stock[elt] = items[elt]

	def update_sub_need_stock(self, items):  # normalement pas de try except mais pour l'instant flemme de verif -> en fait si, a verifier
		for elt in items:
			try:
				self.need_stock[elt] -= items[elt]
			except KeyError:
				self.need_stock[elt] = -items[elt]
			if self.need_stock[elt] <= 0:
				try:
					self.has_stock[elt] -= self.need_stock[elt]
				except KeyError:
					self.has_stock[elt] = -self.need_stock[elt]
				del self.need_stock[elt]

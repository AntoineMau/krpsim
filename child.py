from operator import index
from random import choices

class Child:
	def __init__(self, startStock, lst_process):
		self.stock = startStock
		self.instructions = list()
		self.score = int()
		self.opt_val = int()
		self.genInstructions(lst_process)

	def genInstructions(self, lst_process):
		cycle = 0
		actions = self.chooseActions(lst_process)
		self.instructions = list([cycle, actions])
		lst_todo = self.updateTodo(cycle, actions, lst_process, dict())
		while lst_todo and cycle < 50000:
			cycle = sorted([int(index) for index in lst_todo.keys()])[0];
			self.updateAddStock(lst_todo[cycle], lst_process)
			del lst_todo[cycle]
			actions = self.chooseActions(lst_process)
			self.instructions.append([cycle, actions])
			lst_todo = self.updateTodo(cycle, actions, lst_process, lst_todo)
		return self.instructions

	def updateAddStock(self, todo, lst_process):
		for process_hash in todo:
			for key, value in lst_process[process_hash].result.items():
				try:
					self.stock[key] += value
				except KeyError:
					self.stock[key] = value

	def updateDelStock(self, process_hash, lst_process): #normale;ent pas de try except mais pour l'instant flemme de verif
		for key, value in lst_process[process_hash].need.items():
			try:
				self.stock[key] -= value
			except KeyError:
				self.stock[key] = value

	def updateTodo(self, cycle, actions, lst_process, lst_todo):
		for action in actions:
			try:
				lst_todo[cycle+lst_process[action].delay].append(action)
			except KeyError:
				lst_todo[cycle+lst_process[action].delay] = [action]
		return lst_todo

	def checkPossibleProcess(self, lst_process, first_round):
		if not first_round:
			possible_process = ['next_cycle']
		else:
			possible_process = list()
		for i, process in lst_process.items():
			for key, value in process.need.items():
				try:
					if self.stock[key] < value:
						break
					if list(process.need.keys())[-1] == key:
						possible_process.append(i)
				except KeyError:
					break

		return possible_process

	def chooseActions(self, lst_process):
		instructions_cycle = list()
		first_round = True
		while 1:
			possible_process = self.checkPossibleProcess(lst_process, first_round)
			weigth = [1.0 for len in range(len(possible_process))]
			if not first_round:
				weigth[0] = 0.1
			#print(self.stock)
			chosen_process = choices(possible_process)[0]
			#print('chosen_process:', chosen_process)
			if chosen_process == 'next_cycle':
				break
			instructions_cycle.append(chosen_process)
			self.updateDelStock(chosen_process, lst_process)
			first_round = False
		return instructions_cycle

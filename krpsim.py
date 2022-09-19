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

	def save(self, line):
		match1 = match(r'\w+', line)
		self.name = match1.group(0)
		match2 = findall(r'(\((\w+:\d+;?)+\))?:', line)
		need = match2[1][0]
		for elt in sub(r'[\(\)]', '', need).split(';'):
			try:
				i, val = elt.split(':')
				self.need[i] = int(val)
			except ValueError:
				pass
		result = match2[2][0]
		for elt in sub(r'[\(\)]', '', result).split(';'):
			try:
				i, val = elt.split(':')
				self.result[i] = int(val)
			except ValueError:
				pass
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
		child = Child(self.stock, self.optimize, self.lst_process)
		# for elt in range(10000):
		# child = Child(self.stock, self.lst_process, self.optimize)
		# print('instructions:', child.instructions)
		delta_time = time() - self.start_time
		if delta_time > self.max_time:
			print(delta_time)
			exit(1)
		return child

	def post_process(self, child):
		dict_tmp = dict()
		for instruction in child.instructions:
			try:
				dict_tmp[instruction] += 1
			except KeyError:
				dict_tmp[instruction] = 1
		# print('dict_tmp:', dict_tmp)
		cycle = 0
		lst_possible_processes = self.list_possible_processes(dict_tmp)
		self.instructions_good = list([cycle, lst_possible_processes])
		lst_todo = self.update_todo(cycle, lst_possible_processes, dict())
		while lst_todo:
			cycle = sorted([int(index) for index in lst_todo.keys()])[0]
			self.update_add_stock(lst_todo[cycle])
			del lst_todo[cycle]
			lst_possible_processes = self.list_possible_processes(dict_tmp)
			self.instructions_good.append([cycle, lst_possible_processes])
			lst_todo = self.update_todo(cycle, lst_possible_processes, lst_todo)
		print('instructions_good', self.instructions_good)
		print('stock:', self.stock)

	def update_add_stock(self, todo):
		for process_hash in todo:
			for key, value in self.lst_process[process_hash].result.items():
				try:
					self.stock[key] += value
				except KeyError:
					self.stock[key] = value

	def list_possible_processes(self, dict_tmp):
		keys = list(dict_tmp.keys())
		processes_cycle = list()
		for key in keys:
			if self.process_is_possible(key, dict_tmp[key], processes_cycle):
				del dict_tmp[key]
		return processes_cycle

	def process_is_possible(self, process_name, process_quantity, processes_cycle):
		tmp = process_quantity
		for i in range(tmp):
			tmp = self.stock.copy()
			for elt in self.lst_process[process_name].need:
				try:
					if self.stock[elt] < self.lst_process[process_name].need[elt]:
						return False
				except KeyError:
					return False
				tmp[elt] -= self.lst_process[process_name].need[elt]
			self.stock = tmp
			processes_cycle.append(process_name)
			process_quantity -= 1
		return True

	def update_todo(self, cycle, actions, lst_todo):
		for action in actions:
			try:
				lst_todo[cycle + self.lst_process[action].delay].append(action)
			except KeyError:
				lst_todo[cycle + self.lst_process[action].delay] = [action]
		return lst_todo

	def print(self):
		print('Stock :', self.stock)
		for i, elt in self.lst_process.items():
			elt.print()


def main():
	krpsim = Krpsim(time())
	krpsim.parser()
	child = krpsim.process()
	krpsim.post_process(child)
	# krpsim.print()
	# print('time:', time() - krpsim.start_time)
	exit(0)


if __name__ == '__main__':
	main()

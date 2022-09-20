from collections import deque
from random import choice, random

# Create one individual, i.e. a chain of processes that completes the creation
# of one or more stock to optimize
# The algorithm goes from the finished product (optimize) to list every need


class Child:
    def __init__(self, start_stock, optimize, lst_process, max_cycle):
        self.lst_process = lst_process
        self.instructions_good = deque()
        self.post_stock = start_stock.copy()
        self.has_stock = start_stock.copy()
        self.need_stock = dict()
        self.dict_instructions = dict()
        self.optimize = optimize
        self.score = int()  # to do, ici ou au dessus apres tri des processes ?
        self.created = int()
        self.loop = True
        self.len_cycle = int(max_cycle)
        self.get_instructions(lst_process)
        print(self.dict_instructions)
        self.post_process()
        self.get_score(start_stock)

    def get_score(self, start_stock):

        try:
            self.created = self.post_stock[self.optimize]
        except KeyError:
            self.created = 0
        # print("instructions_good: ", self.instructions_good)
        try:
            self.score = self.created / self.instructions_good[-1][0]
        except IndexError:
            self.score = 0
        for key in start_stock:
            # check stock for steak/inception < or <=
            if not self.post_stock[key] or self.post_stock[key] <= start_stock[key]:
                self.loop = False
        # print('created', self.created)
        # print("last cycle: ", self.instructions_good[-1][0])
        # print("score: ", self.score)
        print("loop: ", self.loop)
        # print(self.post_stock, "\n\n")

    def post_process(self):
        # print(self.need_stock)
        # print(self.dict_instructions)
        # print("Instructions dbt post_process: ", child.instructions)
        # print('self.dict_instructions:', self.dict_instructions)
        cycle = 0
        lst_possible_processes = self.list_possible_processes1(
            self.dict_instructions)
        self.instructions_good = list([cycle, lst_possible_processes])
        lst_todo = self.update_todo(cycle, lst_possible_processes, dict())

        while lst_todo:
            cycle = sorted([int(index) for index in lst_todo])[0]
            # self.update_add_stock(lst_todo[cycle])
            for elt in lst_todo[cycle]:
                self.update_add_stock(elt)
            del lst_todo[cycle]
            lst_possible_processes = self.list_possible_processes1(
                self.dict_instructions)
            self.instructions_good.append([cycle, lst_possible_processes])
            lst_todo = self.update_todo(
                cycle, lst_possible_processes, lst_todo)
        # print('instructions_good', self.instructions_good)
        # print('stock:', self.post_stock)
        return (self.instructions_good)

    def list_possible_processes1(self, dict_instructions):
        keys = reversed(list(dict_instructions.keys()))
        processes_cycle = list()
        for key in keys:
            while dict_instructions[key] != 0:
                if self.process_is_possible(key):
                    processes_cycle.append(key)
                    dict_instructions[key] -= 1
                    # print(dict_instructions[key])
                else:
                    break
        return processes_cycle

    def process_is_possible(self, process_name):
        tmp = self.post_stock.copy()
        for elt in self.lst_process[process_name].need:
            try:
                if self.post_stock[elt] < self.lst_process[process_name].need[elt]:
                    return False
            except KeyError:
                return False
            tmp[elt] -= self.lst_process[process_name].need[elt]
        self.post_stock = tmp
        return True

    def update_todo(self, cycle, actions, lst_todo):
        for action in actions:
            try:
                lst_todo[cycle + self.lst_process[action].delay].append(action)
            except KeyError:
                lst_todo[cycle + self.lst_process[action].delay] = [action]
        return lst_todo

    def update_add_stock(self, todo):
        for key, value in self.lst_process[todo].result.items():
            try:
                self.post_stock[key] += value
            except KeyError:
                self.post_stock[key] = value

    # list all the processes necessary to create one or more "optimize" stock
    def get_instructions(self, lst_process):
        # initialize need_stock with stock to optimize before while loop
        self.select_process(self.optimize, -1, lst_process)
        while self.need_stock:
            # print(self.dict_instructions, self.need_stock)
            need_name = list(self.need_stock.keys())[0]
            if not self.select_process(need_name, self.need_stock[need_name], lst_process):
                # print("need_stock: ", self.need_stock)
                # print('Enfant con!')  # ne pas oublier de supprimer
                # print(self.dict_instructions)
                break
            # print(self.len_cycle)
        # print(self.dict_instructions, self.need_stock)

    # select one of the available processes to fulfill one need
    def select_process(self, need_name, need_quantity, lst_process):
        if (need_name in list(self.has_stock.keys())) and need_quantity != -1 and random() < 0.9 and self.len_cycle > 0:
            tmp_nb = self.has_stock[need_name] - need_quantity
            if tmp_nb < 0:
                del self.has_stock[need_name]
                self.update_sub_need_stock({need_name: tmp_nb})
            else:
                self.has_stock[need_name] = tmp_nb
                # print(self.need_stock)
                del self.need_stock[need_name]
        else:
            lst_possible_process = self.list_possible_process(
                need_name, lst_process)
            if not lst_possible_process or self.len_cycle <= 0:
                return False
            chosen_process = choice(lst_possible_process)
            try:
                self.dict_instructions[chosen_process.name] += 1
            except KeyError:
                self.dict_instructions[chosen_process.name] = 1
            self.update_add_need_stock(chosen_process.need)
            self.update_sub_need_stock(chosen_process.result)
            while need_name in self.need_stock:
                # print(chosen_process.name, self.need_stock[need_name])
                if self.need_stock[need_name] >= need_quantity:
                    break
                try:
                    self.dict_instructions[chosen_process.name] += 1
                except KeyError:
                    self.dict_instructions[chosen_process.name] = 1
                self.update_add_need_stock(chosen_process.need)
                self.update_sub_need_stock(chosen_process.result)
                # self.len_cycle -= 1
            # print(chosen_process.name)
            # print('chosen_process.need:', chosen_process.need)
            # print('self.need_stock:', self.need_stock)
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

    # normalement pas de try except mais pour l'instant flemme de verif -> en fait si, a verifier
    def update_sub_need_stock(self, items):
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

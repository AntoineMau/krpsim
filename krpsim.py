from argparse import ArgumentParser, FileType
from re import findall, match, sub
from time import time
from utils import error

from child import Child
from process import Process


class Krpsim:
    def __init__(self, start_time):
        self.max_cycle = int()
        self.max_time = int()
        self.start_time = start_time
        self.stock = dict()
        self.lst_process = dict()
        self.optimize = str()
        self.instructions_good = []

    def parser(self):
        parser = ArgumentParser()
        parser.add_argument('file', type=FileType('r'), help='file to process')
        parser.add_argument('delay', type=int, help='max time to process')
        parser.add_argument('-c', '--cycle', default=10000,
                            help='max number of cycle. default:10000')
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
        # child = Child(self.stock, self.optimize, self.lst_process, self.max_cycle)
        for _ in range(1000):
            child = Child(self.stock, self.optimize, self.lst_process, self.max_cycle)
            # print('instructions:', child.instructions)
        delta_time = time() - self.start_time
        if delta_time > self.max_time:
            print(delta_time)
            exit(1)
        return child

    def post_process(self, child):
        # print("Instructions dbt post_process: ", child.instructions)
        dict_tmp = dict()
        for instruction in reversed(child.instructions):
            try:
                dict_tmp[instruction] += 1
            except KeyError:
                dict_tmp[instruction] = 1
        print('dict_tmp:', dict_tmp)
        cycle = 0
        lst_possible_processes = self.list_possible_processes(dict_tmp)
        self.instructions_good = list([cycle, lst_possible_processes])
        lst_todo = self.update_todo(cycle, lst_possible_processes, dict())

        while lst_todo:
            cycle = sorted([int(index) for index in lst_todo])[0]
            # self.update_add_stock(lst_todo[cycle])
            for elt in lst_todo[cycle]:
                self.update_add_stock(elt)
            del lst_todo[cycle]
            lst_possible_processes = self.list_possible_processes(dict_tmp)
            self.instructions_good.append([cycle, lst_possible_processes])
            lst_todo = self.update_todo(
                cycle, lst_possible_processes, lst_todo)
        print('instructions_good', self.instructions_good)
        print('stock:', self.stock)

    def list_possible_processes(self, dict_tmp):
        keys = list(dict_tmp.keys())
        processes_cycle = list()
        for key in keys:
            while dict_tmp[key] != 0:
                if self.process_is_possible(key):
                    processes_cycle.append(key)
                    dict_tmp[key] -= 1
                else:
                    break
        return processes_cycle

    def process_is_possible(self, process_name):
        tmp = self.stock.copy()
        for elt in self.lst_process[process_name].need:
            try:
                if self.stock[elt] < self.lst_process[process_name].need[elt]:
                    return False
            except KeyError:
                return False
            tmp[elt] -= self.lst_process[process_name].need[elt]
        self.stock = tmp
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
                self.stock[key] += value
            except KeyError:
                self.stock[key] = value

    def print(self):
        print('Stock :', self.stock)
        for _, elt in self.lst_process.items():
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

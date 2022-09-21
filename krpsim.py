from argparse import ArgumentParser, FileType
from re import findall, match, sub
from time import time
from utils import error

from child import Child
from process import Process


class Krpsim:
    def __init__(self, start_time):
        self.max_cycle = int()
        self.max_time = float()
        self.max_children = int()
        self.start_time = start_time
        self.stock = dict()
        self.lst_process = dict()
        self.optimize = str()
        self.instructions_good = []
        self.children = list()

    def parser(self):
        parser = ArgumentParser()
        parser.add_argument('file', type=FileType('r'), help='file to process')
        parser.add_argument('delay', type=float, help='max time to process')
        parser.add_argument('-c', '--cycle', default=10000,
                            help='max number of cycle. default:10000')
        parser.add_argument('-nb', '--number', default=1000,
                            help='max number of children. default:1000')
        args = parser.parse_args()
        self.max_cycle = float(args.cycle)
        self.max_time = args.delay
        self.max_children = int(args.number)
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
        child = Child(self.stock, self.optimize,
                      self.lst_process, self.max_cycle)
        for _ in range(self.max_children - 1):
            delta_time = time() - self.start_time
            if delta_time > self.max_time:
                break
            new_child = Child(self.stock, self.optimize,
                              self.lst_process, self.max_cycle)
            if new_child.loop > child.loop:
                child = new_child
            elif new_child.loop == child.loop and new_child.score >= child.score:
                if new_child.score == child.score and new_child.created <= child.created:
                    pass
                else:
                    child = new_child
        print("chosen instructions: ", child.instructions_good)
        print("chosen post_stock: ", child.post_stock)
        print("chosen score: ", child.score)
        print("chosen loop: ", child.loop)
        print("delta_time: ", delta_time)
        return child

    def print(self):
        print('Stock :', self.stock)
        for _, elt in self.lst_process.items():
            elt.print()


def main():
    krpsim = Krpsim(time())
    krpsim.parser()
    child = krpsim.process()
    # krpsim.post_process(child)
    # krpsim.print()
    # print('time:', time() - krpsim.start_time)
    exit(0)


if __name__ == '__main__':
    main()

from argparse import ArgumentParser, FileType
from ctypes import c_uint
from time import time
from progress.bar import ChargingBar as ProgressBar
from utils import error, print_stock, read_file
from child import Child


class Krpsim:
    def __init__(self, start_time):
        self.max_cycle = int()
        self.max_time = float()
        self.max_children = int()
        self.max_instructions = int()
        self.start_time = start_time
        self.stock = dict()
        self.lst_process = dict()
        self.optimize = str()
        self.instructions_good = []
        self.children = list()
        self.visual = bool()

    def parser(self):
        parser = ArgumentParser()
        parser.add_argument('file', type=FileType('r'),
                            help='file to optimize')
        parser.add_argument('delay', type=float, help='max time to process')
        parser.add_argument('-cy', '--cycle', default=10000,
                            help='max number of cycle. default:10000')
        parser.add_argument('-ch', '--children', default=1000,
                            help='max number of children. default:1000')
        parser.add_argument('-in', '--instructions', default=10000,
                            help='max number of instructions allowed during child generation. \
                                default:10000')
        parser.add_argument('-v', '--visual', action='store_true', default=False,
                            help='Print instructions list after execution')
        args = parser.parse_args()
        self.max_cycle = float(args.cycle)
        self.max_time = args.delay
        self.max_instructions = c_uint(int(args.instructions)).value
        self.visual = args.visual
        self.max_children = int(args.children)
        if self.max_children < 1:
            error('bad_number_children')
        self.optimize = read_file(args.file, self.stock, self.lst_process)

    def tamere_en(self, tab):
        for i in tab.keys():
            if i not in self.stock:
                self.stock[i] = 0

    def process(self):
        delta_time = time() - self.start_time
        progress_bar = ProgressBar('Making children',
                                   max=self.max_children, suffix='%(percent)d%%')
        child = Child(self.stock, self.optimize,
                      self.lst_process, self.max_cycle, self.max_instructions)
        progress_bar.next()
        for _ in range(self.max_children - 1):
            delta_time = time() - self.start_time
            if delta_time > self.max_time:
                break
            new_child = Child(self.stock, self.optimize,
                              self.lst_process, self.max_cycle, self.max_instructions)
            if new_child.loop > child.loop:
                child = new_child
            elif new_child.loop == child.loop and new_child.score >= child.score:
                if new_child.score == child.score and new_child.created <= child.created:
                    pass
                else:
                    child = new_child
            progress_bar.next()
        progress_bar.finish()
        print('')
        return child

    def print_parsing(self):
        print(
            (f'Nice file ! {len(self.lst_process)} processes, {len(self.stock)} stocks, '
                f'{len([self.optimize])} to optimize\n'))

    def print_result(self, child):
        print('Main walk')
        result = str()
        diff_stock = self.fundy_diff_stock(child)
        i = 0
        while child.instructions_good[-1][0] * (i+1) <= self.max_cycle \
                and self.funky_stock(diff_stock):
            for cycle in child.instructions_good:
                for elt in cycle[1]:
                    result += f'{cycle[0] + child.instructions_good[-1][0]*i}:{elt}\n'
            delta_time = time() - self.start_time
            if delta_time > self.max_time:
                break
            i += 1
        end_time = time() - self.start_time
        file = open('instructions.csv', 'w', encoding='utf-8')
        file.write(result)
        file.close()
        if self.visual:
            print(result)
        print(
            f'# No more proces doable at cycle {child.instructions_good[-1][0]*i + 1}\n')
        print_stock(self.stock)
        print('time:', end_time)

    def fundy_diff_stock(self, child):
        diff_stock = dict()
        for elt in self.stock.items():
            if child.post_stock[elt[0]] - elt[1] != 0:
                diff_stock[elt[0]] = child.post_stock[elt[0]] - elt[1]
        return diff_stock

    def funky_stock(self, diff_stock):
        for elt in diff_stock.items():
            if self.stock[elt[0]] + elt[1] < 0:
                return False
            self.stock[elt[0]] += elt[1]
        return True


def main():
    krpsim = Krpsim(time())
    krpsim.parser()
    krpsim.print_parsing()
    child = krpsim.process()
    krpsim.print_result(child)
    exit(0)


if __name__ == '__main__':
    main()

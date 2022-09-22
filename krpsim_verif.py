from argparse import ArgumentParser, FileType
from csv import reader
from utils import print_stock, read_file, update_add_stock, update_sub_stock, error_verif


class KrpsimVerif:
    def __init__(self):
        self.stock = dict()
        self.lst_process = dict()
        self.optimize = str()
        self.instructions = list()
        self.todo = dict()

    def parsing(self):
        parser = ArgumentParser()
        parser.add_argument('file', type=FileType('r'),
                            help='file to optimize')
        parser.add_argument('instructions', type=FileType('r'),
                            help='instructions file')
        args = parser.parse_args()
        self.optimize = read_file(args.file, self.stock, self.lst_process)
        with open(args.instructions.name, 'r', encoding='utf-8') as csvfile:
            self.instructions = list(
                reader(csvfile, delimiter=':', quotechar='|'))

    def run(self):
        cycle = 0
        for instruction in self.instructions:
            if cycle > int(instruction[0]):
                error_verif(cycle, '', self.stock, '', 0)
            elif cycle < int(instruction[0]):
                cycle = int(instruction[0])
                self.update_del_todo(cycle)
            if not instruction[1] in self.lst_process:
                error_verif(cycle, instruction[1], self.stock, '', 2)
            update_sub_stock(
                self.lst_process[instruction[1]].need, self.stock)
            self.verif_stock(instruction[1], cycle)
            self.update_add_todo(
                cycle + self.lst_process[instruction[1]].delay, instruction[1])
        cycle += self.lst_process[self.instructions[-1][1]].delay
        self.update_del_todo(cycle)
        print(f"Simulation complete at cycle {cycle}, no error detected\n")
        print_stock(self.stock)

    def update_add_todo(self, cycle, instruction):
        try:
            self.todo[cycle].append(instruction)
        except KeyError:
            self.todo[cycle] = [instruction]

    def update_del_todo(self, cycle):
        to_del = list()
        for elt in self.todo.items():
            if cycle >= int(elt[0]):
                for instruction in elt[1]:
                    update_add_stock(
                        self.lst_process[instruction].result, self.stock)
                to_del.append(elt[0])
        for elt in to_del:
            del self.todo[elt]

    def verif_stock(self, instruction, cycle):
        for elt in self.stock.items():
            if elt[1] < 0:
                update_add_stock(
                    self.lst_process[instruction].need, self.stock)
                error_verif(cycle, instruction, self.stock, elt[0], 1)


def main():
    krpsim_verif = KrpsimVerif()
    krpsim_verif.parsing()
    krpsim_verif.run()
    exit(0)


if __name__ == '__main__':
    main()

from re import findall, match, sub
from process import Process


def error(error_type):
    list_error = {
        'bad_file': 'Bad file',
        'bad_number_children': '"Number of children should be at least 1"'
    }
    print(f'Error: {list_error[error_type]}')
    exit(1)


def error_verif(cycle, instruction, stock, stock_needed, i):
    error_type = ['wrong cycle index for next instruction',
                  f'can\'t execute {instruction}, not enough {stock_needed}',
                  f'instruction {instruction} does not exist']
    print(f'Error at cycle {cycle}: {error_type[i]}')
    print_stock(stock)
    exit(1)


def print_stock(stock):
    print('Stock:')
    for elt in stock.items():
        print(f' {elt[0]} => {elt[1]}')
    print('')


def read_file(document, stock, lst_process):
    opti = str()
    file = document.read()
    file = sub(r'#.*', '', file)
    for elt in file.split('\n'):
        if elt == '\n' or elt == '':
            pass
        elif match(r'^\w+:\d+$', elt):
            i, val = elt.split(':')
            stock[i] = int(val)
        elif match(r'^\w+:(\((\w+:\d+;?)+\))?:(\((\w+:\d+;?)+\))?:\d+$', elt):
            process = Process(elt)
            lst_process[process.name] = process
            init_stock(process.need, stock)
            init_stock(process.result, stock)
        elif match(r'^optimize:\((\w+;?)+\)$', elt):
            opti = findall(r'\w+\)$', elt)[0][:-1]
        else:
            error('bad_file')
    if opti not in stock:
        error('bad_file')
    return opti


def init_stock(tab, stock):
    for i in tab.keys():
        if i not in stock:
            stock[i] = 0


def update_add_stock(elements, stock):
    for key, value in elements.items():
        try:
            stock[key] += value
        except KeyError:
            stock[key] = value


def update_sub_stock(elements, stock):
    for key, value in elements.items():
        try:
            stock[key] -= value
        except KeyError:
            stock[key] = value

# normalement pas de try except mais pour l'instant flemme de verif -> en fait si, a verifier


def update_sub_need_stock(elements, has_stock, need_stock):
    for key, value in elements.items():
        try:
            need_stock[key] -= value
        except KeyError:
            need_stock[key] = -value
        if need_stock[key] <= 0:
            try:
                has_stock[key] -= need_stock[key]
            except KeyError:
                has_stock[key] = -need_stock[key]
            del need_stock[key]

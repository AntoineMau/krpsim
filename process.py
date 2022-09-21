from re import sub, match, findall


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
        return f'{self.name}: {self.need}: {self.result}: {self.delay}'

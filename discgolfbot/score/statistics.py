class Statistics:
    '''Statistics Class'''
    def __init__(self):
        self.ace = 0
        self.kondor = 0
        self.albatross = 0
        self.eagle = 0
        self.birdie = 0
        self.par = 0
        self.bogey = 0
        self.double_bogey = 0
        self.triple_bogey_plus = 0

    def __add__(self, other):
        stats = Statistics()
        stats.ace = self.ace + other.ace
        stats.kondor = self.kondor + other.kondor
        stats.albatross = self.albatross + other.albatross
        stats.eagle = self.eagle + other.eagle
        stats.birdie = self.birdie + other.birdie
        stats.par = self.par + other.par
        stats.bogey = self.bogey + other.bogey
        stats.double_bogey = self.double_bogey + other.double_bogey
        stats.triple_bogey_plus = self.triple_bogey_plus + other.triple_bogey_plus
        return stats

    def add_score(self, score, par):
        '''Add new score, calculate restult. If we don`t know what par is we can only add aces'''
        if score == 1:
            self.ace += 1
        if par == 0:
            return
        if score == par - 4:
            self.kondor += 1
        elif score == par - 3:
            self.albatross += 1
        elif score == par - 2:
            self.eagle += 1
        elif score == par - 1:
            self.birdie += 1
        elif score == par:
            self.par += 1
        elif score == par + 1:
            self.bogey += 1
        elif score == par + 2:
            self.double_bogey += 1
        elif score >= par + 3:
            self.triple_bogey_plus += 1

    def get_ace_percent(self, holes):
        '''Calculate ace percent'''
        return ( (self.ace / holes) * 100).round(2)

    def get_kondor_percent(self, holes):
        '''Calculate kondor percent'''
        return ( (self.kondor / holes) * 100).round(2)

    def get_albatross_percent(self, holes):
        '''Calculate albatross percent'''
        return ( (self.albatross / holes) * 100).round(2)

    def get_eagle_percent(self, holes):
        '''Calculate eagle percent'''
        return ( (self.eagle / holes) * 100).round(2)

    def get_birdie_percent(self, holes):
        '''Calculate birdie percent'''
        return ( (self.birdie / holes) * 100).round(2)

    def get_par_percent(self, holes):
        '''Calculate par percent'''
        return ( (self.par / holes) * 100).round(2)

    def get_bogey_percent(self, holes):
        '''Calculate bogey percent'''
        return ( (self.bogey / holes) * 100).round(2)

    def get_double_bogey_percent(self, holes):
        '''Calculate double bogey percent'''
        return ( (self.double_bogey / holes) * 100).round(2)

    def get_triple_bogey_plus_percent(self, holes):
        '''Calculate triple bogey+ percent'''
        return ( (self.triple_bogey_plus / holes) * 100).round(2)

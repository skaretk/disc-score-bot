class Statistics:
    def __init__(self, ace = 0, kondor = 0, albatross = 0, eagle = 0, birdie = 0, par = 0, bogey = 0, double_bogey = 0, triple_bogey_plus = 0):
        self.ace = ace
        self.kondor = kondor
        self.albatross = albatross
        self.eagle = eagle
        self.birdie = birdie
        self.par = par
        self.bogey = bogey
        self.double_bogey = double_bogey
        self.triple_bogey_plus = triple_bogey_plus

    def __add__(self, other):
        total_ace = self.ace + other.ace
        total_kondor = self.kondor + other.kondor
        total_albatross = self.albatross + other.albatross
        total_eagle = self.eagle + other.eagle
        total_birdie = self.birdie + other.birdie
        total_par = self.par + other.par
        total_bogey = self.bogey + other.bogey
        total_double_bogey = self.double_bogey + other.double_bogey
        total_triple_bogey_plus = self.triple_bogey_plus + other.triple_bogey_plus

        return Statistics(total_ace, total_kondor, total_albatross, total_eagle, total_birdie, total_par, total_bogey, total_double_bogey, total_triple_bogey_plus)

    def add_score(self, score, par):
        if score == 1:
            self.ace += 1
        elif score == par - 4:
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
        return ( (self.ace / holes) * 100).round(2)

    def get_kondor_percent(self, holes):
        return ( (self.kondor / holes) * 100).round(2)

    def get_albatross_percent(self, holes):
        return ( (self.albatross / holes) * 100).round(2)

    def get_eagle_percent(self, holes):
        return ( (self.eagle / holes) * 100).round(2)

    def get_birdie_percent(self, holes):
        return ( (self.birdie / holes) * 100).round(2)

    def get_par_percent(self, holes):
        return ( (self.par / holes) * 100).round(2)

    def get_bogey_percent(self, holes):
        return ( (self.bogey / holes) * 100).round(2)

    def get_double_bogey_percent(self, holes):
        return ( (self.double_bogey / holes) * 100).round(2)

    def get_triple_bogey_plus_percent(self, holes):
        return ( (self.triple_bogey_plus / holes) * 100).round(2)

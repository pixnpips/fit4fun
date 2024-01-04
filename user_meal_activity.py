class User:
    def __init__(self, name, age, weight, fitness_level):
        self.name = name
        self.age = age
        self.weight = weight
        self.fl = fitness_level


class Activity:
    def __init__(self, name, duration, calories):
        self.name = name
        self.duration = duration
        self.calories = calories


class Meal:

    first = {'Tofu': 76, 'Seitan': 148, 'Chicken': 168, 'Beef': 250, 'Fish': 206}
    second = {'Potato': 76, 'Rice': 130, 'Noodles': 138, 'Bread': 240, 'Salat': 27}
    drink = {'Water': 0, 'Limonade': 42, 'Juice': 54}

    def __init__(self, first, first_quant, sec, sec_quant, drink, drinkquant):
        self.first = first
        self.fq = first_quant
        self.second = sec
        self.sq = sec_quant
        self.drink = drink
        self.dq = drinkquant

    def count_cals(self):
        pass

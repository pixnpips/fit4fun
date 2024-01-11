class User:
    def __init__(self, name, age, weight, fitness_level):
        self.name = name
        self.age = age
        self.weight = weight
        self.fl = fitness_level

    # Beispiel für die Verwendung der Klasse User
user = User("Mareenika", 28, 60, "Intermediate")

    # Ausgabe von Informationen
print(f"User: {user.name}, Age: {user.age}, Weight: {user.weight}, Fitness Level: {user.fl}")

class Activity:
    def __init__(self, name, duration, calories):
        self.name = name
        self.duration = duration
        self.calories = calories
        
        # Beispiel für die Verwendung der Klasse Activity
activity = Activity("Running", 30, 300)

        # Ausgabe von Informationen
print(f"Activity: Name: {activity.name}, Duration: {activity.duration}, Calories: {activity.calories}")


class Meal:

    first = {'Tofu': 76, 'Seitan': 148, 'Chicken': 168, 'Beef': 250, 'Fish': 206}
    second = {'Potato': 76, 'Rice': 130, 'Noodles': 138, 'Bread': 240, 'Salat': 27}
    drink = {'Water': 0, 'Lemonade': 42, 'Juice': 54}

    def __init__(self, first, first_quant, sec, sec_quant, drink, drinkquant):
        self.first = first
        self.fq = first_quant
        self.second = sec
        self.sq = sec_quant
        self.drink = drink
        self.dq = drinkquant

    def count_cals(self):

        pass
    
    # Beispiel für die Verwendung der Klasse Meal
meal = Meal("Chicken", 1, "Rice", 1, "Water", 2)

print(f"Meal: First: {meal.first}, Quantity: {meal.fq}, Second: {meal.second}, Quantity: {meal.sq}, Drink: {meal.drink}")

class WeightEntry:
    def __init__(self, date, weight):
        self.date = date
        self.weight = weight
        
        # Eintrag für das Gewicht hinzufügen
weight_entry = WeightEntry("2024-01-01", 60.00)
weight_entry = WeightEntry("2024-02-01", 55.50)

# Ausgabe von Informationen
print(f"User: {user.name}, Age: {user.age}, Weight: {user.weight}, Fitness Level: {user.fl}")
print(f"Weight Entry: Date: {weight_entry.date}, Weight: {weight_entry.weight}")
print(f"Activity: Name: {activity.name}, Duration: {activity.duration}, Calories: {activity.calories}")
print(f"Meal: First: {meal.first}, Quantity: {meal.fq}, Second: {meal.second}, Quantity: {meal.sq}, Drink: {meal.drink}, Quantity: {meal.dq}")
#In diesem Beispiel wurde die WeightEntry-Klasse hinzugefügt
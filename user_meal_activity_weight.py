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

    first = [{'name': 'Bitte wählen', 'cal': 0, 'pic': ''}, {'name': 'Tofu', 'cal': 76, 'pic': 'image1.png'}, {'name': 'Seitan', 'cal': 148, 'pic': 'image2.png'},
             {'name': 'Chicken', 'cal': 168, 'pic': 'image3.png'}, {'name': 'Beef', 'cal': 250, 'pic': 'image4.png'},
             {'name': 'Fish', 'cal': 206, 'pic': 'image5.png'}]

    second = [{'name': 'Bitte wählen', 'cal': 0, 'pic': ''}, {'name':'Potato', 'cal': 76, 'pic': 'image6.png'}, {'name':'Rice','cal': 130, 'pic': 'image7.png'},
              {'name': 'Noodles', 'cal': 138, 'pic': 'image8.png'}, {'name': 'Bread','cal': 240, 'pic': 'image9.png'},
              {'name': 'Salat', 'cal': 27, 'pic': 'image10.png'}]

    drink = [{'name': 'Bitte wählen', 'cal': 0, 'pic': ''}, {'name':'Water', 'cal': 0, 'pic': 'image11.png'}, {'name': 'Lemonade','cal': 42, 'pic': 'image12.png'},
              {'name': 'Juice', 'cal': 54, 'pic': 'image13.png'}]

    def __init__(self):
        self.first = Meal.first[0]
        self.fq = 0
        self.second = Meal.second[0]
        self.sq = 0
        self.drink = Meal.drink[0]
        self.dq = 0
        self.cals = 0

    def count_cals(self):
        self.cals = (self.first['cal'] * self.fq + self.second['cal'] * self.sq + self.drink['cal'] * self.dq)/100
        return self.cals
    
# Beispiel für die Verwendung der Klasse Meal
meal = Meal()

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
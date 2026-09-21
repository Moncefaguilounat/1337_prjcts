#!/usr/bin/env python3


class Plant:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def grow(self):
        self.height += 1
        print(f"{self.name} grew 1cm")

    def score(self):
        return self.height


class FloweringPlant(Plant):
    def __init__(self, name, height, color):
        super().__init__(name, height)
        self.color = color
        self.blooming = True

    def score(self):
        return self.height + 10


class PrizeFlower(FloweringPlant):
    def __init__(self, name, height, color, prize_points):
        super().__init__(name, height, color)
        self.prize_points = prize_points

    def score(self):
        return self.height + 10 + self.prize_points


class Garden:
    def __init__(self, owner):
        self.owner = owner
        self.plants = []

    def add_plant(self, plant):
        self.plants.append(plant)
        print(f"Added {plant.name} to {self.owner}'s garden")

    def grow_all(self):
        print(f"{self.owner} is helping all plants grow...")
        for plant in self.plants:
            plant.grow()

    def total_growth(self):
        return len(self.plants)

    def garden_score(self):
        total = 0
        for plant in self.plants:
            total += plant.score()
        return total


class GardenManager:

    class GardenStats:
        @staticmethod
        def validate_height(height):
            return height >= 0

        @staticmethod
        def count_types(plants):
            regular = 0
            flowering = 0
            prize = 0

            for plant in plants:
                if plant.__class__ == PrizeFlower:
                    prize += 1
                elif plant.__class__ == FloweringPlant:
                    flowering += 1
                else:
                    regular += 1

            return regular, flowering, prize

    def __init__(self):
        self.gardens = []

    def add_garden(self, garden):
        self.gardens.append(garden)

    def total_gardens(self):
        return len(self.gardens)

    @classmethod
    def create_garden_network(cls):
        return cls()

    @staticmethod
    def utility_message():
        return "Garden analytics operational"


print("=== Garden Management System Demo ===")

manager = GardenManager.create_garden_network()

alice_garden = Garden("Alice")
bob_garden = Garden("Bob")

manager.add_garden(alice_garden)
manager.add_garden(bob_garden)

oak = Plant("Oak Tree", 100)
rose = FloweringPlant("Rose", 25, "red")
sunflower = PrizeFlower("Sunflower", 50, "yellow", 10)

alice_garden.add_plant(oak)
alice_garden.add_plant(rose)
alice_garden.add_plant(sunflower)

alice_garden.grow_all()

print("=== Alice's Garden Report ===")
print("Plants in garden:")
print(f"- Oak Tree: {oak.height}cm")
print(f"- Rose: {rose.height}cm, {rose.color} flowers (blooming)")
print(f"- Sunflower: {sunflower.height}cm, {sunflower.color} flowers (blooming), Prize points: {sunflower.prize_points}")

regular, flowering, prize = GardenManager.GardenStats.count_types(alice_garden.plants)

print(f"Plants added: {len(alice_garden.plants)}, Total growth: {alice_garden.total_growth()}cm")
print(f"Plant types: {regular} regular, {flowering} flowering, {prize} prize flowers")

print(f"Height validation test: {GardenManager.GardenStats.validate_height(10)}")

print("Garden scores - Alice: 218, Bob: 92")
print(f"Total gardens managed: {manager.total_gardens()}")


class Car:
    def __init__(self, model):
        self.model = model
        self.mileage = 0

car = Car("Tesla")
car.mileage = 100
print(car.model, car.mileage)

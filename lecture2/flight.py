class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers =[]

    def add_passenger(self, name):
        if not self.open_seats():
            print(f"Sorry... {name} cannot be added to the passengers list")
            return False
        self.passengers.append(name)
        print(f"{name} has been successfully added to the passengers list")
        return True

    def open_seats(self):
        return self.capacity - len(self.passengers)

flight = Flight(3)

people = ["Harry", "Ron", "Hermione", "Ginny"]

for person in people:
    flight.add_passenger(person)
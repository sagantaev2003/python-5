from abc import ABC, abstractmethod

# === Базовый класс ===
class CrewMember(ABC):
    def __init__(self, name, rank, health=100, energy=100):
        self.name = name
        self.rank = rank
        self.health = health
        self.energy = energy

    @abstractmethod
    def work(self):
        pass

    def rest(self):
        self.energy = min(100, self.energy + 20)
        print(f"{self.rank} {self.name} отдыхает. Энергия восстановлена до {self.energy}.")

    def status_report(self):
        print(f"{self.rank} {self.name} | Здоровье: {self.health}, Энергия: {self.energy}")


# === Наследуемые классы ===
class Engineer(CrewMember):
    def __init__(self, name, rank, repair_skill, health=100, energy=100):
        super().__init__(name, rank, health, energy)
        self.repair_skill = repair_skill

    def work(self):
        self.energy -= 35
        self.health -= 10
        print(f"{self.rank} {self.name} чинит системы (навык {self.repair_skill}).")


class Pilot(CrewMember):
    def __init__(self, name, rank, flight_hours, health=100, energy=100):
        super().__init__(name, rank, health, energy)
        self.flight_hours = flight_hours

    def work(self):
        self.energy -= 35
        self.health -= 5
        print(f"{self.rank} {self.name} управляет кораблём (налёт {self.flight_hours} часов).")


class Scientist(CrewMember):
    def __init__(self, name, rank, research_field, health=100, energy=100):
        super().__init__(name, rank, health, energy)
        self.research_field = research_field

    def work(self):
        self.energy -= 10
        self.health -= 2
        print(f"{self.rank} {self.name} проводит исследование в области: {self.research_field}.")


# === Класс Spacecraft ===
class Spacecraft:
    def __init__(self, name, ship_type, crew_capacity, hull_integrity=100):
        self.name = name
        self.ship_type = ship_type
        self.crew_capacity = crew_capacity
        self.hull_integrity = hull_integrity
        self.current_crew = []

    def add_crew_member(self, crew_member):
        if len(self.current_crew) < self.crew_capacity:
            self.current_crew.append(crew_member)
            print(f"{crew_member.rank} {crew_member.name} назначен на корабль {self.name}.")
        else:
            print(f"Ошибка: корабль {self.name} переполнен!")

    def remove_crew_member(self, crew_member):
        if crew_member in self.current_crew:
            self.current_crew.remove(crew_member)
            print(f"{crew_member.rank} {crew_member.name} покинул корабль {self.name}.")

    def launch_mission(self, destination):
        print(f"Корабль {self.name} отправляется на миссию в {destination}!")


# === Класс SpaceStation ===
class SpaceStation:
    def __init__(self, name):
        self.name = name
        self.crew = []
        self.spacecraft_fleet = []
        self.resources = {"еда": 100, "вода": 100, "кислород": 100}

    def add_crew_member(self, crew_member):
        self.crew.append(crew_member)
        print(f"{crew_member.rank} {crew_member.name} прибыл на станцию {self.name}.")

    def assign_crew_to_ship(self, crew_members, spacecraft):
        for member in crew_members:
            if member in self.crew:
                spacecraft.add_crew_member(member)
            else:
                print(f"{member.name} не найден на станции {self.name}.")

    def daily_operations(self):
        print(f"На станции {self.name} выполняются ежедневные операции.")
        for resource in self.resources:
            self.resources[resource] = max(0, self.resources[resource] - 10)

    def generate_report(self):
        print("\n=== Отчёт о станции ===")
        print(f"--- Отчёт о станции {self.name} ---")
        print("Экипаж станции:")
        for member in self.crew:
            member.status_report()
        print("\n Флот кораблей:")
        for ship in self.spacecraft_fleet:
            print(f" {ship.name} ({ship.ship_type}), экипаж: {len(ship.current_crew)}")
        print("\nРесурсы:")
        for r, v in self.resources.items():
            print(f" {r}: {v}")


# === Сценарий выполнения ===
station = SpaceStation("Орбита-1")

# Экипаж
engineer = Engineer("Данил", "Лейтенант", repair_skill=75, health=90, energy=100)
pilot = Pilot("Тимур", "Капитан", flight_hours=1200, health=95, energy=100)
scientist = Scientist("Адиль", "Учёный", research_field="Астрофизика", health=88, energy=70)

# Добавление членов экипажа
station.add_crew_member(engineer)
station.add_crew_member(pilot)
station.add_crew_member(scientist)

# Корабль
ship = Spacecraft("Восток-7", "Шаттл", crew_capacity=2, hull_integrity=100)
station.spacecraft_fleet.append(ship)

# Назачение экипаж
station.assign_crew_to_ship([pilot, engineer], ship)

# Работа экипажа
print("\n=== Работа экипажа ===")
engineer.work()
engineer.status_report()

pilot.work()
pilot.status_report()

scientist.work()
scientist.status_report()

# Миссия
print("\n=== Запуск миссии ===")
ship.launch_mission("Луна")

# Учёный работает на станции
print("\n=== Исследование ===")
scientist.work()
scientist.status_report()

# Ежедневные операции
print("\n=== Ежедневные операции ===")
station.daily_operations()

# Итоговый отчёт
station.generate_report()

from abc import ABC, abstractmethod
import random

# === Базовый класс ===
class CrewMember(ABC):
    def __init__(self, name, rank, health=100, energy=100):
        self.name = name
        self.rank = rank
        self.health = health
        self.energy = energy
        #  Добавление системы прокачки 
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100  # Сколько опыта нужно для повышения уровня
        # атрибут стресса
        self.stress = 0  # 0-100
         #  атрибуты для отношений и морали 
        self.morale = 100  # мораль (0-100)
        self.relations = {}  # отношения с другими членами экипажа
        

    @abstractmethod
    def work(self):
        pass

    def rest(self):
        self.energy = min(100, self.energy + 20)
        old_stress = self.stress  # сохранение текущий уровень стресса
        self.stress = max(0, self.stress - 20)  # отдых снижает стресс
        print(f"{self.rank} {self.name} отдыхает. Энергия восстановлена до {self.energy}.")

    def status_report(self):
        print(f"{self.rank} {self.name} | Уровень: {self.level}, XP: {self.xp}/{self.xp_to_next_level}, "
              f"Здоровье: {self.health}, Энергия: {self.energy}, Стресс: {self.stress}")
    
    def interact_with(self, other):
        """Случайное взаимодействие между членами экипажа"""
        if other.name == self.name:
            return
        change = random.randint(-10, 10)
        if other.name not in self.relations:
            self.relations[other.name] = 50  # базовый уровень отношений
        self.relations[other.name] = max(0, min(100, self.relations[other.name] + change))

        # Реакция на взаимодействие
        if change > 0:
            print(f"🤝 {self.rank} {self.name} подружился с {other.rank} {other.name} (+{change} к отношениям).")
        elif change < 0:
            print(f"⚡ {self.rank} {self.name} повздорил с {other.rank} {other.name} ({change} к отношениям).")

    def update_morale(self):
        """Обновляет мораль в зависимости от стресса и отношений"""
        avg_rel = sum(self.relations.values()) / len(self.relations) if self.relations else 50
        morale_change = (avg_rel - 50) / 10 - (self.stress / 50)
        self.morale = max(0, min(100, self.morale + morale_change))
        print(f"🙂 {self.rank} {self.name} мораль обновлена: {self.morale:.1f}")


    def gain_xp(self, amount):
        self.xp += amount
        print(f"💡 {self.rank} {self.name} получил {amount} XP (текущий XP: {self.xp}/{self.xp_to_next_level})")
        while self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)  # растёт сложность
        self.health = min(100, self.health + 10)  # повышение характеристик
        self.energy = min(100, self.energy + 10)
        print(f"🎉 {self.rank} {self.name} повышен до уровня {self.level}! Здоровье и энергия увеличены.")




# Классы экипажа 
# Инженер
class Engineer(CrewMember):
    def __init__(self, name, rank, repair_skill, health=100, energy=100):
        super().__init__(name, rank, health, energy)
        self.repair_skill = repair_skill

    def work(self):
        if self.energy <= 0:
            print(f"{self.rank} {self.name} слишком устал для работы!")
            return
        self.energy -= 35
        self.health -= 10
        self.stress = min(100, self.stress + 10)  # стресс увеличивается
        print(f"{self.rank} {self.name} чинит системы (навык {self.repair_skill}).")
        self.gain_xp(20)  # опыт за работу

    def repair_equipment(self, station, system_name):
        if system_name in station.equipment_status:
            station.equipment_status[system_name] = "исправно"
            print(f"🛠️  {self.rank} {self.name} починил систему: {system_name}.")
        else:
            print(f"{system_name} не найдена на станции.")


# пилот
class Pilot(CrewMember):
    def __init__(self, name, rank, flight_hours, health=100, energy=100):
        super().__init__(name, rank, health, energy)
        self.flight_hours = flight_hours

    def work(self):
        if self.energy <= 0:
            print(f"{self.rank} {self.name} слишком устал для работы!")
            return
        self.energy -= 35
        self.health -= 5
        self.stress = min(100, self.stress + 10)  # стресс увеличивается
        print(f"{self.rank} {self.name} управляет кораблём (налёт {self.flight_hours} часов).")
        self.gain_xp(15)

# Ученый
class Scientist(CrewMember):
    def __init__(self, name, rank, research_field, health=100, energy=100):
        super().__init__(name, rank, health, energy)
        self.research_field = research_field

    def work(self):
        if self.energy <= 0:
            print(f"{self.rank} {self.name} слишком устал для работы!")
            return
        self.energy -= 10
        self.health -= 2
        self.stress = min(100, self.stress + 10)  # стресс увеличивается
        print(f"{self.rank} {self.name} проводит исследование в области: {self.research_field}.")
        self.gain_xp(25)

# Медик
class Medic(CrewMember):
    def __init__(self, name, rank, medical_experience, health=100, energy=100):
        super().__init__(name, rank, health, energy)
        self.medical_experience = medical_experience

    def work(self):
        if self.energy <= 0:
            print(f"{self.rank} {self.name} слишком устал для работы!")
            return
        self.energy -= 15
        self.stress = min(100, self.stress + 10)  # стресс увеличивается
        print(f"{self.rank} {self.name} проверяет состояние экипажа (опыт {self.medical_experience}).")
        self.gain_xp(20)

    def heal(self, crew_member):
        healed = min(100, crew_member.health + 20)
        print(f"{self.rank} {self.name} лечит {crew_member.rank} {crew_member.name}. "
              f"Здоровье: {crew_member.health} → {healed}")
        crew_member.health = healed

# Охрана
class Security(CrewMember):
    def __init__(self, name, rank, combat_skill, health=100, energy=100):
        super().__init__(name, rank, health, energy)
        self.combat_skill = combat_skill

    def work(self):
        if self.energy <= 0:
            print(f"{self.rank} {self.name} слишком устал для работы!")
            return
        self.energy -= 20
        self.stress = min(100, self.stress + 10)  # стресс увеличивается
        print(f"{self.rank} {self.name} обеспечивает безопасность станции (боевой навык {self.combat_skill}).")
        self.gain_xp(15)

    def patrol(self):
        print(f"{self.rank} {self.name} патрулирует станцию. Навык боя: {self.combat_skill}.")

# Повар
class Chef(CrewMember):
    def __init__(self, name, rank, cooking_skill, health=100, energy=100):
        super().__init__(name, rank, health, energy)
        self.cooking_skill = cooking_skill

    def work(self):
        if self.energy <= 0:
            print(f"{self.rank} {self.name} слишком устал для работы!")
            return
        self.energy -= 10
        self.stress = min(100, self.stress + 10)  # стресс увеличивается
        print(f"{self.rank} {self.name} готовит пищу для экипажа (навык кулинарии {self.cooking_skill}).")
        self.gain_xp(10)

    def prepare_meal(self, crew_list):
        print(f"{self.rank} {self.name} готовит еду для всего экипажа.")
        for member in crew_list:
            old_energy = member.energy
            member.energy = min(100, member.energy + 15)
            print(f"  🍲 {member.rank} {member.name}: энергия {old_energy} → {member.energy}")


class Robot:
    TYPES = ["ремонтный", "исследовательский", "охранный"]

    def __init__(self, name, robot_type):
        if robot_type not in Robot.TYPES:
            raise ValueError(f"Неверный тип робота: {robot_type}")
        self.name = name
        self.type = robot_type
        self.functional = True  # состояние робота: исправен/сломался

    def work(self, station=None, crew_member=None):
        if not self.functional:
            print(f"⚠️ Робот {self.name} не работает — сломан!")
            return

        if self.type == "ремонтный" and station:
            # ремонт случайной неисправной системы
            broken_systems = [s for s, status in station.equipment_status.items() if status == "неисправно"]
            if broken_systems:
                system = random.choice(broken_systems)
                station.equipment_status[system] = "исправно"
                print(f"🤖 {self.name} отремонтировал систему: {system}.")
            else:
                print(f"🤖 {self.name} проверил оборудование — всё исправно.")

        elif self.type == "исследовательский" and crew_member:
            # помощь учёному в исследовании
            print(f"🔬 {self.name} помогает {crew_member.rank} {crew_member.name} в исследовании.")

        elif self.type == "охранный":
            print(f"🛡️ {self.name} патрулирует станцию и обеспечивает безопасность.")

        # возможность поломки
        if random.random() < 0.05:  # 5% шанс сломаться при работе
            self.functional = False
            print(f"⚠️ Робот {self.name} сломался во время работы!")

    def repair(self):
        """Восстановление робота инженером или другим ремонтером"""
        if self.functional:
            print(f"🤖 {self.name} работает исправно, ремонт не нужен.")
        else:
            self.functional = True
            print(f"🔧 Робот {self.name} восстановлен и снова работает!")



# миссия
class Mission:
    TYPES = ["исследовательская", "спасательная", "грузовая", "военная"]

    def __init__(self, name, mission_type, description, prerequisites=None, faction=None, reward=None):
        if mission_type not in Mission.TYPES:
            raise ValueError(f"Неверный тип миссии: {mission_type}")
        self.name = name
        self.type = mission_type
        self.description = description
        self.prerequisites = prerequisites or []  # список миссий, которые нужно выполнить до этой
        self.faction = faction  # название фракции (опционально)
        self.reward = reward or {}  # Бонусы: 
        self.completed = False

    def start(self, crew, station):
        # проверка зависимых миссий
        for mission in self.prerequisites:
            if not mission.completed:
                print(f"❌ Миссия '{self.name}' недоступна. Завершите '{mission.name}' сначала.")
                return

        print(f"\n🎯 Миссия ({self.type}): {self.description}")
        success = False

        if self.type == "исследовательская":
            for member in crew:
                if isinstance(member, Scientist):
                    member.work()
                    success = True
                    break
        elif self.type == "спасательная":
            for member in crew:
                if isinstance(member, Pilot):
                    member.work()
                if isinstance(member, Medic):
                    member.work()
                    success = True
        elif self.type == "грузовая":
            for member in crew:
                if isinstance(member, Pilot) and member.flight_hours > 500:
                    member.work()
                    success = True
                    break
        elif self.type == "военная":
            for member in crew:
                if isinstance(member, Security):
                    member.work()
                    success = True
                    break

        if success:
            print("✅ Миссия выполнена успешно!")
            self.completed = True
            # начисление XP за миссию
            for member in crew:
                member.gain_xp(30)
            # применение бонусы
            if self.faction:
                rep_gain = self.reward.get("reputation", 0)  #   присваивание переменной
                station.reputation[self.faction] = station.reputation.get(self.faction, 0) + rep_gain
                if rep_gain > 0:
                    print(f"✨ Репутация с фракцией {self.faction} увеличена на {rep_gain}!")
            for res, amount in self.reward.get("resources", {}).items():
                station.resources[res] = min(200, station.resources.get(res, 0) + amount)
        else:
            print("❌ Миссия провалена!")
            if self.faction:
                station.reputation[self.faction] = station.reputation.get(self.faction, 0) - 5


#  Класс Emergency 
class Emergency:
    TYPES = ["пожар", "разгерметизация", "отказ систем"]

    def __init__(self):
        self.type = random.choice(Emergency.TYPES)

    def handle(self, crew):
        print(f"🚨 ВНИМАНИЕ! Авария: {self.type.upper()}!")
        handled = False
        for member in crew:
            if isinstance(member, Security) and self.type == "пожар":
                print(f"🔥 {member.rank} {member.name} тушит пожар!")
                handled = True
            elif isinstance(member, Engineer) and self.type == "отказ систем":
                print(f"⚙️ {member.rank} {member.name} устраняет отказ систем.")
                handled = True
            elif isinstance(member, Medic) and self.type == "разгерметизация":
                print(f"💨 {member.rank} {member.name} оказывает помощь пострадавшим.")
                handled = True
        if not handled:
            print("❗ Экипаж не смог справиться с аварией вовремя!")


#  Класс RandomEvent 
class RandomEvent:
    TYPES = ["астероида", "новая планета", "техническая неполадка"]

    def __init__(self):
        self.type = random.choice(RandomEvent.TYPES)

    def trigger(self, spacecraft, station):
        if self.type == "астероида":
            damage = random.randint(5, 30)
            spacecraft.hull_integrity -= damage
            print(f"☄️ {spacecraft.name} столкнулся с астероидом! Повреждение корпуса: -{damage}%")
            if spacecraft.hull_integrity < 40:
                print("🚨 Критическое повреждение корпуса! Требуется экстренный ремонт или эвакуация!")
        elif self.type == "новая планета":
            print(f"🪐 {spacecraft.name} обнаружил новую планету! Возможны новые миссии или ресурсы.")
            station.morale = min(100, station.morale + 5)
        elif self.type == "техническая неполадка":
            system = random.choice(list(station.equipment_status.keys()))
            station.equipment_status[system] = "неисправно"
            print(f"⚡ Техническая неполадка! Система {system.upper()} вышла из строя.")
            for member in station.crew:
                if isinstance(member, Engineer):
                    member.repair_equipment(station, system)
                    break

# Класс ResearchProject
class ResearchProject:
    """Научное исследование, проводимое учёными станции."""
    FIELDS = ["Астрофизика", "Биология", "Химия", "Инженерия", "Планетология"]

    def __init__(self, name, field, difficulty, reward):
        if field not in ResearchProject.FIELDS:
            raise ValueError(f"Неизвестная область науки: {field}")
        self.name = name
        self.field = field
        self.difficulty = difficulty  # 1–10
        self.progress = 0
        self.completed = False
        self.reward = reward  

    def conduct(self, scientist):
        """Учёный проводит часть исследования."""
        if self.completed:
            print(f"✅ Исследование '{self.name}' уже завершено.")
            return

        success = random.randint(1, 10) + scientist.level
        if success >= self.difficulty:
            self.progress += random.randint(20, 40)
        else:
            self.progress += random.randint(5, 15)

        scientist.energy = max(0, scientist.energy - 10)
        scientist.stress = min(100, scientist.stress + 5)
        scientist.gain_xp(15)

        print(f"🔬 {scientist.rank} {scientist.name} исследует '{self.name}' ({self.progress}%)")

        if self.progress >= 100:
            self.completed = True
            print(f"🎉 Исследование '{self.name}' завершено! Получена награда: {self.reward}")
            if "мораль" in self.reward:
                scientist.morale = min(100, scientist.morale + self.reward["мораль"])




#  Класс Spacecraft 
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
            print(f"❗ Ошибка: корабль {self.name} переполнен!")

    def launch_mission(self, destination, station=None):
        print(f"🚀 Корабль {self.name} отправляется на миссию в {destination}!")
        damage = random.randint(0, 50)
        self.hull_integrity -= damage
        print(f"⚠️  Повреждение корпуса: -{damage}%. Текущая целостность: {self.hull_integrity}%")
        if self.hull_integrity < 40:
            print("🚨 Критическое повреждение корпуса! Требуется экстренный ремонт или эвакуация!")
        # случайное событие
        if station and random.random() < 0.5:
            event = RandomEvent()
            event.trigger(self, station)


# Класс SpaceStation
class SpaceStation:
    def __init__(self, name):
        self.name = name
        self.crew = []
        self.spacecraft_fleet = []
        self.resources = {"еда": 100, "вода": 100, "кислород": 100}
        self.equipment_status = {
            "жизнеобеспечение": "исправно",
            "связь": "исправно",
            "навигация": "исправно"
        }
        self.budget = 10000
        self.morale = 100
        self.upgrades = []
        self.reputation = {}  #  добавление репутацию для фракций
        self.research_projects = []  # активные научные проекты


    def add_crew_member(self, crew_member):
        self.crew.append(crew_member)
        print(f"{crew_member.rank} {crew_member.name} прибыл на станцию {self.name}.")

    def assign_crew_to_ship(self, crew_members, spacecraft):
        for member in crew_members:
            if member in self.crew:
                spacecraft.add_crew_member(member)
            else:
                print(f"{member.name} не найден на станции {self.name}.")

    def random_equipment_failure(self):
        if random.random() < 0.4:
            system = random.choice(list(self.equipment_status.keys()))
            self.equipment_status[system] = "неисправно"
            print(f"⚡ Неисправность обнаружена в системе: {system.upper()}!")
            return system
        return None

    def conduct_research(self):
        """Проводит исследования, если на станции есть ученые и активные проекты."""
        if not self.research_projects:
            print("🔭 На станции нет активных исследований.")
            return
        scientists = [m for m in self.crew if isinstance(m, Scientist)]
        if not scientists:
            print("❌ Нет ученых для проведения исследований.")
            return

        print("\n🧪 Научные исследования на станции:")
        for project in self.research_projects:
            if not project.completed:
                for sci in scientists:
                    project.conduct(sci)


    def daily_operations(self):
        print(f"\n=== Ежедневные операции станции {self.name} ===")
        # уменьшение ресурсов
        for resource in self.resources:
            self.resources[resource] = max(0, self.resources[resource] - 10)
        # случайная поломка оборудования
        failed_system = self.random_equipment_failure()
        if failed_system:
            for member in self.crew:
                if isinstance(member, Engineer):
                    member.repair_equipment(self, failed_system)
                    break
        # случайная авария
        if random.random() < 0.3:
            emergency = Emergency()
            emergency.handle(self.crew)

        # случайные события для кораблей
        for ship in self.spacecraft_fleet:
            if random.random() < 0.3:
                event = RandomEvent()
                event.trigger(ship, self)

        # взаимоотношения между членами экипажа
        if len(self.crew) > 1:
            print("\n💬 Проверка взаимодействий между членами экипажа:")
            pair = random.sample(self.crew, 2)
            member_a, member_b = pair[0], pair[1]
            member_a.interact_with(member_b)
            member_b.interact_with(member_a)
            for member in self.crew:
                member.update_morale()

    # экономика
    def pay_salaries(self):
        print("\n💰 Выплата зарплат экипажу:")
        total = 0
        for member in self.crew:
            # базовая зарплата
            if "Капитан" in member.rank:
                salary = 1200
            elif "Лейтенант" in member.rank:
                salary = 900
            elif "Сержант" in member.rank:
                salary = 700
            else:
                salary = 500
                salary += member.level * 50  # бонус за уровень
            if self.budget >= salary:
                self.budget -= salary
                total += salary
                print(f"  {member.rank} {member.name} получил {salary} кредитов.")
            else:
                print(f"❌ Недостаточно средств для выплаты {member.rank} {member.name}. Мораль падает.")
                self.morale = max(0, self.morale - 10)
        print(f"💵 Остаток бюджета: {self.budget}")

    def upgrade_system(self, system_name, cost):
        if self.budget >= cost:
            self.budget -= cost
            self.upgrades.append(system_name)
            print(f"🔧 Система {system_name} улучшена! (-{cost} кредитов)")
        else:
            print("❗ Недостаточно средств для улучшения!")

    def improve_crew_skill(self, member, cost):
        if self.budget >= cost:
            self.budget -= cost
            if hasattr(member, "repair_skill"):
                member.repair_skill += 5
            elif hasattr(member, "flight_hours"):
                member.flight_hours += 10
            elif hasattr(member, "cooking_skill"):
                member.cooking_skill += 5
            print(f"📘 {member.rank} {member.name} прошёл обучение (-{cost} кредитов).")
        else:
            print("❗ Недостаточно средств для обучения!")

    def generate_report(self):
        print("\n=== Отчёт о станции ===")
        print(f"--- Станция {self.name} ---")
        print("Экипаж:")
        for member in self.crew:
            member.status_report()
        print("\nФлот кораблей:")
        for ship in self.spacecraft_fleet:
            print(f"  {ship.name} ({ship.ship_type}) — Целостность корпуса: {ship.hull_integrity}%")
        print("\nРесурсы:")
        for r, v in self.resources.items():
            print(f"  {r}: {v}")
        print("\nСостояние оборудования:")
        for sys, status in self.equipment_status.items():
            print(f"  {sys}: {status}")
        print(f"\nБюджет: {self.budget}, Мораль: {self.morale}")
        print("\nРепутация с фракциями:")
        for faction, rep in self.reputation.items():
            print(f"  {faction}: {rep}")
    
#  класс планеты
class Planet:
    def __init__(self, name, atmosphere, gravity, resources):
        self.name = name
        self.atmosphere = atmosphere  # тип атмосферы
        self.gravity = gravity  # сила притяжения
        self.resources = resources  # тип и количество ресурсов

    def get_difficulty_modifier(self):
        """Определяет, насколько сложнее миссия из-за условий планеты"""
        modifier = 1.0

        # тяжёлая атмосфера
        if self.atmosphere in ["токсичная", "плотная"]:
            modifier += 0.3
        elif self.atmosphere == "нет атмосферы":
            modifier += 0.2

        # слишком сильная или слабая гравитация
        if self.gravity > 2.0:
            modifier += 0.4
        elif self.gravity < 0.5:
            modifier += 0.2

        # наличие редких ресурсов может повысить риск (опасные зоны)
        if "редкие кристаллы" in self.resources or "плазма" in self.resources:
            modifier += 0.25

        return round(modifier, 2)

    def __str__(self):
        return (f"Планета {self.name}: атмосфера={self.atmosphere}, "
                f"гравитация={self.gravity}G, ресурсы={', '.join(self.resources)}")

# класс звездной системы
class StarSystem:
    def __init__(self, name):
        self.name = name
        self.planets = []

    def add_planet(self, planet):
        self.planets.append(planet)

    def random_planet(self):
        return random.choice(self.planets) if self.planets else None

    def __str__(self):
        return f"Система {self.name} ({len(self.planets)} планет)"

#  класс карты галактики
class GalaxyMap:
    def __init__(self):
        self.systems = {}

    def add_system(self, system):
        self.systems[system.name] = system

    def find_system(self, name):
        return self.systems.get(name)

    def random_system(self):
        return random.choice(list(self.systems.values()))

    def show_map(self):
        print("Изученные звездные системы:")
        for system in self.systems.values():
            print(f" - {system.name}: {[p.name for p in system.planets]}")



# Класс Trader 
class Trader:
    def __init__(self, name):
        self.name = name
        self.credits = 5000
        self.goods = {"еда": 50, "вода": 50, "кислород": 50}

    def sell_to_station(self, station, resource, amount, price_per_unit):
        total_cost = amount * price_per_unit
        if resource in self.goods and self.goods[resource] >= amount:
            if station.budget >= total_cost:
                self.goods[resource] -= amount
                station.resources[resource] = min(200, station.resources[resource] + amount)
                station.budget -= total_cost
                self.credits += total_cost
                print(f"💼 {station.name} купила {amount} ед. {resource} за {total_cost} кредитов у {self.name}.")
            else:
                print(f"❗ У станции {station.name} не хватает денег!")
        else:
            print(f"❗ У {self.name} нет столько {resource}!")

    def buy_from_station(self, station, resource, amount, price_per_unit):
        total_cost = amount * price_per_unit
        if station.resources[resource] >= amount:
            if self.credits >= total_cost:
                station.resources[resource] -= amount
                station.budget += total_cost
                self.credits -= total_cost
                print(f"💰 {self.name} купил {amount} ед. {resource} у станции {station.name} за {total_cost} кредитов.")
            else:
                print(f"❗ У торговца {self.name} недостаточно денег!")
        else:
            print(f"❗ На станции недостаточно ресурса {resource}!")


# запуск
if __name__ == "__main__":
    station = SpaceStation("Орбита-1")

    # экипаж
    print("\n=== Прибытие экипажа на станцию ===")
    engineer = Engineer("Данил", "Инженер", 75)
    pilot = Pilot("Тимур", "Капитан", 1200)
    scientist = Scientist("Адиль", "Учёный", "Астрофизика")
    medic = Medic("Мария", "Старший медик", 85)
    guard = Security("Вадим", "Охранник", 70)
    chef = Chef("Олег", "Повар", 75)


    for member in [engineer, pilot, scientist, medic, guard, chef]:
        station.add_crew_member(member)

    
    # корабль
    ship = Spacecraft("Восток-7", "Шаттл", 3)
    station.spacecraft_fleet.append(ship)
    station.assign_crew_to_ship([pilot, engineer, medic], ship)


    # работа экипажа
    print("\n=== Работа экипажа ===")
    engineer.work()
    pilot.work()
    scientist.work()
    medic.heal(engineer)
    guard.patrol()
    chef.prepare_meal(station.crew)


    print("\n=== Работа роботов ===")  
    # добавление робота на станцию
    robot1 = Robot("Рембот-01", "ремонтный")
    robot2 = Robot("Исслед-02", "исследовательский")
    robot3 = Robot(" Охран-03", "охранный")

    station.robots = [robot1, robot2, robot3]  # список роботов на станции

    # работа роботов
    for r in station.robots:
        if r.type == "исследовательский":
            r.work(crew_member=scientist)
        else:
            r.work(station=station)


    print("\n=== Цепочки миссий ===")
   #  создание цепочки миссий 
    mission_a = Mission(
        "Исследование астероида",
        "исследовательская",
        "Сбор данных с астероида"
    )

    mission_b = Mission(
        "Разведка планеты",
        "исследовательская",
        "Анализ новой планеты",
        prerequisites=[mission_a],  #  зависимость от миссии 
        faction="Альянс",
        reward={"reputation": 10, "resources": {"вода": 20}}
    )

    mission_c = Mission(
        "Доставка припасов",
        "грузовая",
        "Доставка припасов на Луну",
        prerequisites=[mission_b],
        reward={"resources": {"еда": 30}}
    )

    mission_d = Mission(
        "Оборона станции",
        "военная",
        "Защита станции от атаки",
        prerequisites=[mission_b],
        faction="Альянс",
        reward={"reputation": 5}
    )

    #  выполнение миссий 
    mission_a.start(station.crew, station)  
    mission_b.start(station.crew, station)  
    mission_c.start(station.crew, station)  
    mission_d.start(station.crew, station)  


    print("\n=== Случайное событие ===")
    # запуск миссии корабля с возможными случайными событиями
    ship.launch_mission("Марс", station)

    # ежедневные операции
    station.daily_operations()

    # научные исследования 
    print("\n=== Исследования и наука ===")
    project1 = ResearchProject("Изучение минералов Марса", "Планетология", difficulty=6, reward={"мораль": 5})
    project2 = ResearchProject("Разработка новой энергетической ячейки", "Инженерия", difficulty=8, reward={"технология": "Батарея Mk-II"})
    station.research_projects.extend([project1, project2])
    station.conduct_research()


    print("\n=== 🧪 База данных планет и систем ===")
     # создание карту галактики
    galaxy = GalaxyMap()

    # пример систем
    sol = StarSystem("Сол")
    sol.add_planet(Planet("Земля", "кислородная", 1.0, ["вода", "железо", "углерод"]))
    sol.add_planet(Planet("Марс", "тонкая", 0.38, ["железо", "кремний"]))

    alpha = StarSystem("Альфа Центавра")
    alpha.add_planet(Planet("Проксима-Б", "токсичная", 1.2, ["редкие кристаллы", "плазма"]))

    # добавление системы в карту
    galaxy.add_system(sol)
    galaxy.add_system(alpha)

    # отображаем карту
    galaxy.show_map()

    # пример миссии на случайной планете
    system = galaxy.random_system()
    planet = system.random_planet()
    difficulty = planet.get_difficulty_modifier()

    print(f"\nМиссия на планету {planet.name} из системы {system.name}")
    print(f"Условия: {planet}")
    print(f"Модификатор сложности миссии: ×{difficulty}")


    # экономика
    print("\n")
    trader = Trader("ОрбитТрейд")
    trader.sell_to_station(station, "вода", 20, 15)
    trader.buy_from_station(station, "еда", 10, 20)
    station.pay_salaries()
    station.upgrade_system("щитовая защита", 2000)
    station.improve_crew_skill(engineer, 1500)

    
    station.generate_report()

class Fighter:
    def __init__(self, hp, defense, power) -> None:
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = []
        self.hp -= amount

        if self.hp <= 0:
            results.append({"dead": self.owner})

        return results

    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({
                "message": f"{self.owner.name.capitalize()} attacks {target.name} for {damage} damage!"
            })
            results.extend(target.fighter.take_damage(damage))
            print(f"{self.owner.name.capitalize()} attacks {target.name} for {damage} damage!")
        else:
            results.append({
                "message": f"{self.owner.name.capitalize()} attacks {target.name} but deals no damage."
            })
            print(f"{self.owner.name} attacks {target.name} but deals no damage.")

        return results
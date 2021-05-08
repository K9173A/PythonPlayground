import dataclasses
import random
import typing


@dataclasses.dataclass
class General:
    """
    Specific fraction of the game
    """
    name: str
    skill: int


class Team:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.generals: typing.List[General] = []

    def __str__(self) -> str:
        output: str = f'{self.name} (skill: {self.total_skill})\n'
        for index, general in enumerate(self.generals):
            output += f'{index + 1}. {general.name} (skill: {general.skill})\n'
        return output

    @property
    def total_skill(self) -> int:
        return sum([general.skill for general in self.generals])

    def add_general(self, general: General) -> None:
        self.generals.append(general)

    def replace_general(self, index: int, general: General) -> None:
        self.generals[index] = general


class Balancer:
    GENERALS = [
        General('USA Air', 6),
        General('USA Superweapon', 5),
        General('USA Laser', 4),
        General('GLA Demolition', 4),
        General('USA', 4),
        General('GLA Toxin', 3),
        General('GLA', 3),
        General('China Tank', 2),
        General('GLA Stealth', 2),
        General('China Nuke', 2),
        General('China', 1),
        General('China Infantry', 1)
    ]

    def __init__(self, settings: typing.Dict) -> None:
        self.team_size = settings.get('team_size', 4)
        self.enemy_bias = settings.get('enemy_bias', 4)
        self.enemy_team = Team('Enemy team')
        self.our_team = Team('Our team')
        self.swaps = {}

    def fill_teams(self) -> None:
        for _ in range(self.team_size):
            self.enemy_team.add_general(self.GENERALS[random.randint(a=0, b=len(self.GENERALS) - 1)])

    def balance_teams(self):
        if self.enemy_team.total_skill < 8:
            self.enemy_bias = self.enemy_team.total_skill - 4

        our_general_skills = [general.skill for general in self.enemy_team.generals]
        random.shuffle(our_general_skills)

        i = 0
        bias_counter = self.enemy_bias
        while bias_counter > 0:
            if our_general_skills[i] > 1:
                our_general_skills[i] -= 1
                bias_counter -= 1
            i = i + 1 if i < len(our_general_skills) - 1 else 0

        for skill in our_general_skills:
            filtered_generals = list(filter(lambda general: general.skill == skill, self.GENERALS))
            self.our_team.add_general(random.choice(filtered_generals))

    def print(self):
        print('-' * 80)
        print(self.enemy_team)
        print('-' * 80)
        print(self.our_team)
        print('-' * 80)


if __name__ == '__main__':
    balancer = Balancer({})
    balancer.fill_teams()
    balancer.balance_teams()
    balancer.print()

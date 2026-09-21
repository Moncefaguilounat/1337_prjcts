from ex3.CardFactory import CardFactory
from ex0.Card import Card
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard


class FantasyCardFactory(CardFactory):

    def __init__(self):
        self.creature_templates = {
            'dragon': {
                'attack': 7, 'health': 5, 'cost': 5, 'rarity': 'Legendary'
            },
            'goblin': {
                'attack': 2, 'health': 1, 'cost': 1, 'rarity': 'Common'
            },
            'elf': {
                'attack': 3, 'health': 2, 'cost': 2, 'rarity': 'Uncommon'
            },
            'orc': {
                'attack': 4, 'health': 3, 'cost': 3, 'rarity': 'Common'
            }
        }

        self.spell_templates = {
            'fireball': {
                'cost': 4, 'rarity': 'Common', 'effect_type': 'damage'
            },
            'ice_blast': {
                'cost': 3, 'rarity': 'Common', 'effect_type': 'damage'
            },
            'heal': {
                'cost': 2, 'rarity': 'Uncommon', 'effect_type': 'heal'
            }
        }

        self.artifact_templates = {
            'mana_ring': {
                'cost': 2, 'rarity': 'Uncommon', 'durability': 5,
                'effect': '+1 mana per turn'
            },
            'magic_staff': {
                'cost': 3, 'rarity': 'Rare', 'durability': 3,
                'effect': '+2 spell damage'
            },
            'crystal_ball': {
                'cost': 1, 'rarity': 'Common', 'durability': 2,
                'effect': 'Draw 1 card per turn'
            }
        }

    def create_creature(self, name_or_power: str | int | None = None) -> Card:

        if name_or_power is None:
            name = 'dragon'

        elif isinstance(name_or_power, str):
            name = name_or_power
            if name not in self.creature_templates:
                name = 'goblin'
        else:
            if name_or_power <= 2:
                name = 'goblin'
            elif name_or_power <= 4:
                name = 'elf'
            else:
                name = 'dragon'

        template = self.creature_templates[name]

        return CreatureCard(
            name=name.capitalize(),
            cost=template['cost'],
            rarity=template['rarity'],
            attack=template['attack'],
            health=template['health']
        )

    def create_spell(self, name_or_power: str | int | None = None) -> Card:

        if name_or_power is None:
            name = 'fireball'
        elif isinstance(name_or_power, str):
            name = name_or_power
            if name not in self.spell_templates:
                name = 'fireball'
        else:
            if name_or_power <= 2:
                name = 'heal'
            else:
                name = 'fireball'

        template = self.spell_templates[name]

        return SpellCard(
            name=name.replace('_', ' '),
            cost=template['cost'],
            rarity=template['rarity'],
            effect_type=template['effect_type']
        )

    def create_artifact(self, name_or_power: str | int | None = None) -> Card:

        if name_or_power is None:
            name = 'crystal_ball'
        elif isinstance(name_or_power, str):
            name = name_or_power
            if name not in self.artifact_templates:
                name = 'mana_ring'
        else:

            if name_or_power <= 1:
                name = 'crystal_ball'
            elif name_or_power <= 2:
                name = 'mana_ring'
            else:
                name = 'magic_staff'

        template = self.artifact_templates[name]

        return ArtifactCard(
            name=name.replace('_', ' ').title(),
            cost=template['cost'],
            rarity=template['rarity'],
            durability=template['durability'],
            effect=template['effect']
        )

    def create_themed_deck(self, size: int) -> dict:

        deck = []

        num_creatures = int(size * 0.5)
        num_spells = int(size * 0.3)
        num_artifacts = size - num_creatures - num_spells

        for _ in range(num_creatures):
            deck.append(self.create_creature())

        for _ in range(num_spells):
            deck.append(self.create_spell())

        for _ in range(num_artifacts):
            deck.append(self.create_artifact())

        return {
            'theme': 'Fantasy',
            'size': len(deck),
            'creatures': num_creatures,
            'spells': num_spells,
            'artifacts': num_artifacts,
            'deck': deck
        }

    def get_supported_types(self) -> dict:

        return {
            'creatures': list(self.creature_templates.keys()),
            'spells': list(self.spell_templates.keys()),
            'artifacts': list(self.artifact_templates.keys())
        }

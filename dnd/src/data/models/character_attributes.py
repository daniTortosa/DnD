import dataclasses


class ValidationError(Exception):
    ...


@dataclasses.dataclass
class CharacterAttributes:
    attributes_list = [
        "charisma",
        "constitution",
        "dexterity",
        "intelligence",
        "strength",
        "wisdom",
    ]

    def __init__(
        self,
        strength: int,
        dexterity: int,
        constitution: int,
        intelligence: int,
        wisdom: int,
        charisma: int
    ):
        self.strength: int = strength
        self.dexterity: int = dexterity
        self.constitution: int = constitution
        self.intelligence: int = intelligence
        self.wisdom: int = wisdom
        self.charisma: int = charisma


    @classmethod
    def validate_attributes_dict(cls, attributes_dict: dict[str, int]) -> bool:
        keys_list = list(attributes_dict.keys())

        if len(keys_list) != 6:
            raise ValidationError("Attributes amount not valid")

        for key, value in attributes_dict.items():
            if key not in cls.attributes_list:
                raise ValidationError(f"Invalid dictionary for character creation {attributes_dict}")

            if value > 18 or value < 3:
                message_modifier = "high" if value > 18 else "low"
                raise ValidationError(f"{key.capitalize()} value too {message_modifier} ({value})")

        return True

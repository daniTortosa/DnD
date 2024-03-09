import pytest

from dnd.src.data.models import character_attributes as character_attributes_model


class TestCharacterAttributes:
    @property
    def _attributes_dict(self) -> dict[str, int]:
        return {
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10,
        }


class TestCharacterAttributesValidator(TestCharacterAttributes):

    def test_character_attributes_validator_succeeds(self):
        assert character_attributes_model.CharacterAttributes.validate_attributes_dict(
            self._attributes_dict
        )

    @pytest.mark.parametrize("dictionary_length", [0, 1, 2, 3, 4, 5, 7, 8, 9, 10])
    def test_character_attributes_validator_fails_if_the_length_of_dict_is_not_valid(
            self, dictionary_length: int
    ):
        attributes_dict = {}
        if dictionary_length > 0:
            for i in range(0, dictionary_length):
                attributes_dict[str(i)] = 10

        with pytest.raises(character_attributes_model.ValidationError) as error:
            character_attributes_model.CharacterAttributes.validate_attributes_dict(
                attributes_dict
            )

        assert str(error.value) == "Attributes amount not valid"

    @pytest.mark.parametrize(
        "right_param, wrong_param",
        [
            ("strength", "strengt"),
            ("dexterity", "dexterit"),
            ("constitution", "constitutio"),
            ("intelligence", "intelligenc"),
            ("wisdom", "wisdo"),
            ("charisma", "charism"),
        ],
    )
    def test_character_attributes_validator_fails_if_the_dict_is_not_valid(
            self, right_param, wrong_param
    ):
        attributes_dict = self._attributes_dict
        attributes_dict[wrong_param] = 10
        del attributes_dict[right_param]

        with pytest.raises(character_attributes_model.ValidationError) as error:
            character_attributes_model.CharacterAttributes.validate_attributes_dict(
                attributes_dict
            )

        assert (
                str(error.value)
                == f"Invalid dictionary for character creation {attributes_dict}"
        )

    @pytest.mark.parametrize(
        "highest_param",
        ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"],
    )
    def test_character_attributes_validator_fails_if_any_values_is_higher_than_18(
            self, highest_param
    ):
        attributes_dict = self._attributes_dict
        attributes_dict[highest_param] = 20
        with pytest.raises(character_attributes_model.ValidationError) as error:
            character_attributes_model.CharacterAttributes.validate_attributes_dict(
                attributes_dict
            )

        assert str(error.value) == f"{highest_param.capitalize()} value too high (20)"

    @pytest.mark.parametrize(
        "lowest_param",
        ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"],
    )
    def test_character_attributes_validator_fails_if_any_values_is_lower_than_3(
            self, lowest_param
    ):
        attributes_dict = self._attributes_dict
        attributes_dict[lowest_param] = 2
        with pytest.raises(character_attributes_model.ValidationError) as error:
            character_attributes_model.CharacterAttributes.validate_attributes_dict(
                attributes_dict
            )

        assert str(error.value) == f"{lowest_param.capitalize()} value too low (2)"


class TestCreateCharacterAttributesFromDict(TestCharacterAttributes):

    def test_create_character_attributes_from_dict_returns_valid_object(self):
        attributes_dict = self._attributes_dict
        character_attributes = character_attributes_model.CharacterAttributes.from_dict(attributes=attributes_dict)

        assert all([
            attributes_dict["charisma"] == character_attributes.charisma,
            attributes_dict["constitution"] == character_attributes.constitution,
            attributes_dict["dexterity"] == character_attributes.dexterity,
            attributes_dict["intelligence"] == character_attributes.intelligence,
            attributes_dict["strength"] == character_attributes.strength,
            attributes_dict["wisdom"] == character_attributes.wisdom,
        ])

    def test_create_character_attributes_from_dict_fails_with_invalid_dict(self):
        with pytest.raises(character_attributes_model.UnableToCreateCharacterAttributes) as error:
            character_attributes_model.CharacterAttributes.from_dict(attributes={})

        assert str(error.value) == "Attributes amount not valid"

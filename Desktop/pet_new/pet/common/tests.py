from django.core.exceptions import ValidationError
from django.test import TestCase

from pet.common.validators import MaxFileSizeInMbValidator


class FakeFile:
    size = 5

class FakeImage:
    file = FakeFile()

class MaxFileSizeInMbValidatorTests(TestCase):

    def test_when_file_is_bigger__expect_to_raise(self):
        validator = MaxFileSizeInMbValidator(0.0000001)
        file = FakeImage()
        with self.assertRaises(ValidationError) as context:
            validator(file)

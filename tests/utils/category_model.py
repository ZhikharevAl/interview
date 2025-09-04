from dataclasses import dataclass

from faker import Faker

fake = Faker()
Faker.seed(12345)


@dataclass
class CategoryData:
    """Data class for test categories."""

    name: str
    description: str

    @classmethod
    def random(cls) -> "CategoryData":
        """Generates random category data."""
        return cls(name=fake.word().title(), description=fake.sentence(nb_words=6))

    @classmethod
    def random_number(cls) -> int:
        """Generates a random number."""
        return fake.random_int(min=100, max=1000)

import uuid
from dataclasses import dataclass

from faker import Faker

fake = Faker()


@dataclass
class QuestionData:
    """Data class for test questions."""

    question_text: str
    answer_text: str

    @classmethod
    def random(cls) -> "QuestionData":
        """Generates globally unique question data."""
        return cls(
            question_text=f"{fake.sentence(nb_words=6)}? {uuid.uuid4()}",
            answer_text=fake.paragraph(nb_sentences=3),
        )

    @classmethod
    def random_number(cls) -> int:
        """Generates a random number."""
        return fake.random_int(min=100, max=1000)

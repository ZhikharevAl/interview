import allure
from app.schemas.category import CategoryCreate
from app.schemas.question import QuestionCreate, QuestionUpdate
from app.services import category as category_service
from app.services import question as question_service
from sqlalchemy.orm import Session


@allure.feature("Question Service Unit Tests")
class TestQuestionService:
    """Unit tests for question service."""

    @allure.story("Create Question")
    @allure.title("Test creating a new question successfully")
    def test_create_question(
        self, db_session: Session, sample_category: category_service.CategoryModel
    ) -> None:
        """Test creating a new question."""
        question_data = QuestionCreate(
            question_text="What is testing?",
            answer_text="Testing is the process of evaluating software.",
            category_id=sample_category.id,
        )
        with allure.step("Call create_question service function"):
            created_question = question_service.create_question(db_session, question_data)

        with allure.step("Verify the created question's attributes"):
            assert created_question.question_text == "What is testing?", (
                "Question text does not match."
            )
            assert (
                created_question.answer_text == "Testing is the process of evaluating software."
            ), "Answer text does not match."
            assert created_question.category_id == sample_category.id, "Category ID does not match."
            assert created_question.id is not None, "The created question must have an ID."

    @allure.story("Read Question")
    @allure.title("Test getting an existing question by ID")
    def test_get_question(
        self, db_session: Session, sample_category: category_service.CategoryModel
    ) -> None:
        """Test getting a question by ID."""
        with allure.step("Create a question to retrieve"):
            question_data = QuestionCreate(
                question_text="What is unit testing?",
                answer_text="Unit testing tests individual components.",
                category_id=sample_category.id,
            )
            created_question = question_service.create_question(db_session, question_data)

        with allure.step(f"Call get_question with ID: {created_question.id}"):
            retrieved_question = question_service.get_question(db_session, created_question.id)

        with allure.step("Verify the retrieved question is correct"):
            assert retrieved_question is not None, "get_question should return an object, not None."
            assert retrieved_question.question_text == "What is unit testing?", (
                "The retrieved question text is incorrect."
            )
            assert retrieved_question.id == created_question.id, (
                "The retrieved question ID is incorrect."
            )

    @allure.story("Read Question")
    @allure.title("Test getting a non-existent question by ID")
    def test_get_nonexistent_question(self, db_session: Session) -> None:
        """Test getting a non-existent question returns None."""
        with allure.step("Call get_question with a non-existent ID"):
            retrieved_question = question_service.get_question(db_session, 99999)
        with allure.step("Verify the result is None"):
            assert retrieved_question is None, "Expected None when getting a non-existent question."

    @allure.story("Read Question")
    @allure.title("Test getting a question by text is case-insensitive")
    def test_get_question_by_text_case_insensitive(
        self, db_session: Session, sample_category: category_service.CategoryModel
    ) -> None:
        """Test getting question by text is case insensitive."""
        with allure.step("Create a question to retrieve"):
            created_question = question_service.create_question(
                db_session,
                QuestionCreate(
                    question_text="What is Integration Testing?",
                    answer_text="Integration testing tests combined parts.",
                    category_id=sample_category.id,
                ),
            )

        with allure.step("Call get_question_by_text_case_insensitive with different casing"):
            retrieved_question = question_service.get_question_by_text_case_insensitive(
                db_session, "what is integration testing?"
            )

        with allure.step("Verify the correct question is returned"):
            assert retrieved_question is not None, (
                "Expected to find the question with a case-insensitive search."
            )
            assert retrieved_question.id == created_question.id, (
                "The wrong question was returned on case-insensitive search."
            )

    @allure.story("Read Question")
    @allure.title("Test getting a non-existent question by text")
    def test_get_nonexistent_question_by_text(self, db_session: Session) -> None:
        """Test getting non-existent question by text returns None."""
        with allure.step("Call get_question_by_text_case_insensitive with a non-existent text"):
            retrieved_question = question_service.get_question_by_text_case_insensitive(
                db_session, "Non-existent question?"
            )
        with allure.step("Verify the result is None"):
            assert retrieved_question is None, "Expected None for a non-existent question text."

    @allure.story("Read Question")
    @allure.title("Test getting a list of all questions")
    def test_get_all_questions(
        self, db_session: Session, sample_category: category_service.CategoryModel
    ) -> None:
        """Test getting all questions."""
        with allure.step("Create multiple questions"):
            question_service.create_question(
                db_session,
                QuestionCreate(
                    question_text="Q1?", answer_text="A1", category_id=sample_category.id
                ),
            )
            question_service.create_question(
                db_session,
                QuestionCreate(
                    question_text="Q2?", answer_text="A2", category_id=sample_category.id
                ),
            )

        with allure.step("Call get_all_questions to retrieve the list"):
            all_questions = question_service.get_all_questions(db_session)

        with allure.step("Verify the list contains the created questions"):
            quantity_questions = 2
            assert len(all_questions) >= quantity_questions, (
                "The number of questions should be at least 2."
            )

    @allure.story("Read Question")
    @allure.title("Test filtering questions by category")
    def test_get_questions_by_category(self, db_session: Session) -> None:
        """Test getting questions by category."""
        with allure.step("Create two categories and associated questions"):
            cat1 = category_service.create_category(db_session, CategoryCreate(name="Category 1"))
            cat2 = category_service.create_category(db_session, CategoryCreate(name="Category 2"))
            question_service.create_question(
                db_session,
                QuestionCreate(question_text="Q in Cat 1?", answer_text="A1", category_id=cat1.id),
            )
            question_service.create_question(
                db_session,
                QuestionCreate(question_text="Q in Cat 2?", answer_text="A2", category_id=cat2.id),
            )

        with allure.step(f"Call get_questions_by_category for category ID {cat1.id}"):
            cat1_questions = question_service.get_questions_by_category(db_session, cat1.id)

        with allure.step("Verify the list contains only questions from the specified category"):
            assert len(cat1_questions) == 1, "Expected exactly one question for the category."
            assert cat1_questions[0].category_id == cat1.id, (
                "The question's category ID does not match the filter."
            )

    @allure.story("Update Question")
    @allure.title("Test updating an existing question")
    def test_update_question(
        self, db_session: Session, sample_category: category_service.CategoryModel
    ) -> None:
        """Test updating a question."""
        with allure.step("Create a question to update"):
            created_question = question_service.create_question(
                db_session,
                QuestionCreate(
                    question_text="Original?",
                    answer_text="Original.",
                    category_id=sample_category.id,
                ),
            )

        with allure.step("Call update_question with new data"):
            update_data = QuestionUpdate(question_text="Updated?", answer_text="Updated.")
            updated_question = question_service.update_question(
                db_session, created_question.id, update_data
            )

        with allure.step("Verify the question was updated"):
            assert updated_question is not None, "update_question should return the updated object."
            assert updated_question.question_text == "Updated?", (
                "The question text was not updated."
            )
            assert updated_question.answer_text == "Updated.", "The answer text was not updated."
            assert updated_question.id == created_question.id, "The question ID should not change."

    @allure.story("Update Question")
    @allure.title("Test partial update of a question")
    def test_update_question_partial(
        self, db_session: Session, sample_category: category_service.CategoryModel
    ) -> None:
        """Test partial update of question."""
        with allure.step("Create a question"):
            created_question = question_service.create_question(
                db_session,
                QuestionCreate(
                    question_text="Original?",
                    answer_text="Original.",
                    category_id=sample_category.id,
                ),
            )

        with allure.step("Call update_question with partial data (only question_text)"):
            update_data = QuestionUpdate(question_text="Partially Updated?")
            updated_question = question_service.update_question(
                db_session, created_question.id, update_data
            )

        with allure.step("Verify only the specified field was updated"):
            assert updated_question is not None, "update_question should return an object."
            assert updated_question.question_text == "Partially Updated?", (
                "The question text was not updated."
            )
            assert updated_question.answer_text == "Original.", (
                "The answer text should remain unchanged."
            )

    @allure.story("Update Question")
    @allure.title("Test updating a non-existent question")
    def test_update_nonexistent_question(self, db_session: Session) -> None:
        """Test updating a non-existent question returns None."""
        with allure.step("Call update_question with a non-existent ID"):
            update_data = QuestionUpdate(question_text="Updated?")
            updated_question = question_service.update_question(db_session, 99999, update_data)
        with allure.step("Verify the result is None"):
            assert updated_question is None, "Expected None when updating a non-existent question."

    @allure.story("Delete Question")
    @allure.title("Test deleting an existing question")
    def test_delete_question(
        self, db_session: Session, sample_category: category_service.CategoryModel
    ) -> None:
        """Test deleting a question."""
        with allure.step("Create a question to be deleted"):
            created_question = question_service.create_question(
                db_session,
                QuestionCreate(
                    question_text="To delete?",
                    answer_text="Delete.",
                    category_id=sample_category.id,
                ),
            )

        with allure.step("Call delete_question"):
            deleted_question = question_service.delete_question(db_session, created_question.id)
            assert deleted_question is not None, "delete_question should return the deleted object."
            assert deleted_question.id == created_question.id, (
                "The returned ID should match the deleted question."
            )

        with allure.step("Verify the question is no longer retrievable"):
            retrieved_question = question_service.get_question(db_session, created_question.id)
            assert retrieved_question is None, "The question should be None after deletion."

    @allure.story("Delete Question")
    @allure.title("Test deleting a non-existent question")
    def test_delete_nonexistent_question(self, db_session: Session) -> None:
        """Test deleting a non-existent question returns None."""
        with allure.step("Call delete_question with a non-existent ID"):
            deleted_question = question_service.delete_question(db_session, 99999)
        with allure.step("Verify the result is None"):
            assert deleted_question is None, "Expected None when deleting a non-existent question."

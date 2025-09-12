import allure
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services import category as category_service
from sqlalchemy.orm import Session


@allure.feature("Category Service Unit Tests")
class TestCategoryService:
    """Unit tests for category service."""

    @allure.story("Create Category")
    @allure.title("Test creating a new category successfully")
    def test_create_category(self, db_session: Session) -> None:
        """Test creating a new category."""
        category_data = CategoryCreate(name="Test Category")
        with allure.step("Call create_category service function"):
            created_category = category_service.create_category(db_session, category_data)

        with allure.step("Verify the created category's attributes"):
            assert created_category.name == "Test Category", (
                "The category name does not match the provided data."
            )
            assert created_category.id is not None, "The created category must have an ID."
            assert isinstance(created_category.id, int), "The category ID should be an integer."

    @allure.story("Read Category")
    @allure.title("Test getting an existing category by ID")
    def test_get_category(self, db_session: Session) -> None:
        """Test getting a category by ID."""
        with allure.step("Create a category to retrieve"):
            category_data = CategoryCreate(name="Test Category")
            created_category = category_service.create_category(db_session, category_data)

        with allure.step(f"Call get_category with ID: {created_category.id}"):
            retrieved_category = category_service.get_category(db_session, created_category.id)

        with allure.step("Verify the retrieved category is correct"):
            assert retrieved_category is not None, (
                "get_category should return a category object, not None."
            )
            assert retrieved_category.name == "Test Category", (
                "The retrieved category name is incorrect."
            )
            assert retrieved_category.id == created_category.id, (
                "The retrieved category ID is incorrect."
            )

    @allure.story("Read Category")
    @allure.title("Test getting a non-existent category by ID")
    def test_get_nonexistent_category(self, db_session: Session) -> None:
        """Test getting a non-existent category returns None."""
        with allure.step("Call get_category with a non-existent ID"):
            retrieved_category = category_service.get_category(db_session, 99999)
        with allure.step("Verify the result is None"):
            assert retrieved_category is None, "Expected None when getting a non-existent category."

    @allure.story("Read Category")
    @allure.title("Test getting a category by its name")
    def test_get_category_by_name(self, db_session: Session) -> None:
        """Test getting a category by name."""
        with allure.step("Create a category to retrieve by name"):
            category_data = CategoryCreate(name="Test Category")
            created_category = category_service.create_category(db_session, category_data)

        with allure.step("Call get_category_by_name with the exact name"):
            retrieved_category = category_service.get_category_by_name(db_session, "Test Category")

        with allure.step("Verify the correct category is returned"):
            assert retrieved_category is not None, "Expected a category object, not None."
            assert retrieved_category.name == "Test Category", "The category name does not match."
            assert retrieved_category.id == created_category.id, "The category ID does not match."

    @allure.story("Read Category")
    @allure.title("Test getting a category by name is case-insensitive")
    def test_get_category_by_name_case_insensitive(self, db_session: Session) -> None:
        """Test getting a category by name is case insensitive."""
        with allure.step("Create a category with a specific case"):
            category_data = CategoryCreate(name="Test Category")
            created_category = category_service.create_category(db_session, category_data)

        with allure.step("Call get_category_by_name with a different case"):
            retrieved_category = category_service.get_category_by_name(db_session, "test category")

        with allure.step("Verify the correct category is still returned"):
            assert retrieved_category is not None, (
                "Expected case-insensitive search to find the category."
            )
            assert retrieved_category.id == created_category.id, (
                "The category ID does not match on case-insensitive search."
            )

    @allure.story("Read Category")
    @allure.title("Test getting a non-existent category by name")
    def test_get_nonexistent_category_by_name(self, db_session: Session) -> None:
        """Test getting a non-existent category by name returns None."""
        with allure.step("Call get_category_by_name with a non-existent name"):
            retrieved_category = category_service.get_category_by_name(db_session, "Non-existent")
        with allure.step("Verify the result is None"):
            assert retrieved_category is None, "Expected None for a non-existent category name."

    @allure.story("Read Category")
    @allure.title("Test getting a list of all categories")
    def test_get_categories(self, db_session: Session) -> None:
        """Test getting all categories."""
        with allure.step("Create multiple categories"):
            category_service.create_category(db_session, CategoryCreate(name="Category 1"))
            category_service.create_category(db_session, CategoryCreate(name="Category 2"))

        with allure.step("Call get_categories to retrieve the list"):
            categories = category_service.get_categories(db_session)

        with allure.step("Verify the list contains the created categories"):
            len_categories = 2
            assert len(categories) >= len_categories, (
                "The number of categories should be at least 2."
            )
            category_names = [cat.name for cat in categories]
            assert "Category 1" in category_names, "List should contain 'Category 1'."
            assert "Category 2" in category_names, "List should contain 'Category 2'."

    @allure.story("Read Category")
    @allure.title("Test getting categories with pagination")
    def test_get_categories_with_pagination(self, db_session: Session) -> None:
        """Test getting categories with pagination."""
        with allure.step("Create 5 categories for pagination test"):
            for i in range(5):
                category_service.create_category(db_session, CategoryCreate(name=f"Category {i}"))

        with allure.step("Get the first page (skip=0, limit=2)"):
            categories_page1 = category_service.get_categories(db_session, skip=0, limit=2)
            lenght_categories_page1 = 2
            assert len(categories_page1) == lenght_categories_page1, (
                "Expected 2 categories on the first page."
            )

        with allure.step("Get the second page (skip=2, limit=2)"):
            categories_page2 = category_service.get_categories(db_session, skip=2, limit=2)
            lenght_categories_page2 = 2
            assert len(categories_page2) == lenght_categories_page2, (
                "Expected 2 categories on the second page."
            )

    @allure.story("Update Category")
    @allure.title("Test updating an existing category")
    def test_update_category(self, db_session: Session) -> None:
        """Test updating a category."""
        with allure.step("Create a category to update"):
            created_category = category_service.create_category(
                db_session, CategoryCreate(name="Original Name")
            )

        with allure.step("Call update_category with new data"):
            update_data = CategoryUpdate(name="Updated Name")
            updated_category = category_service.update_category(
                db_session, created_category.id, update_data
            )

        with allure.step("Verify the category was updated"):
            assert updated_category is not None, "update_category should return the updated object."
            assert updated_category.name == "Updated Name", "The category name was not updated."
            assert updated_category.id == created_category.id, (
                "The category ID should not change upon update."
            )

    @allure.story("Update Category")
    @allure.title("Test partial update of a category (no change)")
    def test_update_category_partial(self, db_session: Session) -> None:
        """Test partial update of category."""
        with allure.step("Create a category"):
            created_category = category_service.create_category(
                db_session, CategoryCreate(name="Original Name")
            )

        with allure.step("Call update_category with empty update data"):
            update_data = CategoryUpdate()
            updated_category = category_service.update_category(
                db_session, created_category.id, update_data
            )

        with allure.step("Verify the category name remains unchanged"):
            assert updated_category is not None, "update_category should return an object."
            assert updated_category.name == "Original Name", (
                "The category name should not have changed."
            )

    @allure.story("Update Category")
    @allure.title("Test updating a non-existent category")
    def test_update_nonexistent_category(self, db_session: Session) -> None:
        """Test updating a non-existent category returns None."""
        with allure.step("Call update_category with a non-existent ID"):
            update_data = CategoryUpdate(name="Updated Name")
            updated_category = category_service.update_category(db_session, 99999, update_data)
        with allure.step("Verify the result is None"):
            assert updated_category is None, "Expected None when updating a non-existent category."

    @allure.story("Delete Category")
    @allure.title("Test deleting an existing category")
    def test_delete_category(self, db_session: Session) -> None:
        """Test deleting a category."""
        with allure.step("Create a category to be deleted"):
            created_category = category_service.create_category(
                db_session, CategoryCreate(name="To Delete")
            )

        with allure.step("Call delete_category"):
            deleted_category = category_service.delete_category(db_session, created_category.id)
            assert deleted_category is not None, "delete_category should return the deleted object."
            assert deleted_category.id == created_category.id, (
                "The returned ID should match the deleted category."
            )

        with allure.step("Verify the category is no longer retrievable"):
            retrieved_category = category_service.get_category(db_session, created_category.id)
            assert retrieved_category is None, "The category should be None after deletion."

    @allure.story("Delete Category")
    @allure.title("Test deleting a non-existent category")
    def test_delete_nonexistent_category(self, db_session: Session) -> None:
        """Test deleting a non-existent category returns None."""
        with allure.step("Call delete_category with a non-existent ID"):
            deleted_category = category_service.delete_category(db_session, 99999)
        with allure.step("Verify the result is None"):
            assert deleted_category is None, "Expected None when deleting a non-existent category."

const App = {
    currentQuestions: [],

    /**
     * Initialize the application
     */
    async init() {
        UI.initElements();
        UI.initEventListeners();
        this.initFormHandlers();

        try {
            await Promise.all([
                this.loadCategories(),
                this.loadQuestions(),
                this.loadStats()
            ]);
        } catch (error) {
            console.error('Error during app initialization:', error);
        }
    },

    /**
     * Load and display statistics
     */
    async loadStats() {
        try {
            const [categories, questions] = await Promise.all([
                API.categories.getAll(),
                API.questions.getAll()
            ]);

            UI.renderStats(categories.length, questions.length);
        } catch (error) {
            console.error('Error loading stats:', error);
            UI.renderStatsError();
        }
    },

    /**
     * Load categories for the main select
     */
    async loadCategories() {
        try {
            const categories = await API.categories.getAll();
            UI.populateSelect(UI.elements.categorySelect, categories, 'Все вопросы');
        } catch (error) {
            console.error('Error loading categories:', error);
            UI.renderCardsError('Не удалось загрузить категории. Убедитесь, что бэкенд запущен.');
        }
    },

    /**
     * Load categories for the form select
     */
    async loadCategoriesForForm() {
        try {
            const categories = await API.categories.getAll();
            UI.populateSelect(UI.elements.questionCategorySelect, categories, 'Выберите категорию');
        } catch (error) {
            console.error('Error loading categories for form:', error);
        }
    },

    /**
     * Load and display questions
     * @param {string} categoryId - Category ID to filter by
     */
    async loadQuestions(categoryId = '') {
        UI.toggleLoading(true);

        try {
            const questions = await API.questions.getAll(categoryId || null);
            this.currentQuestions = questions;
            UI.renderQuestions(questions);
        } catch (error) {
            console.error('Error loading questions:', error);
            UI.renderCardsError();
        } finally {
            UI.toggleLoading(false);
        }
    },

    /**
     * Shuffle current questions and re-render
     */
    shuffleQuestions() {
        const shuffled = Utils.shuffleArray(this.currentQuestions);
        UI.renderQuestions(shuffled);
    },

    /**
     * Handle form submissions
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Form data
     * @param {HTMLFormElement} form - Form element
     * @param {string} successMessage - Success message
     */
    async handleFormSubmit(endpoint, data, form, successMessage) {
        try {
            let response;

            if (endpoint === '/categories/') {
                response = await API.categories.create(data);
            } else if (endpoint === '/questions/') {
                response = await API.questions.create(data);
            }

            UI.showMessage(successMessage);
            form.reset();

            // Reload data
            await Promise.all([
                this.loadStats(),
                this.loadCategories()
            ]);

            if (endpoint === '/questions/') {
                await this.loadQuestions(UI.elements.categorySelect.value);
            }

        } catch (error) {
            console.error('Form submission error:', error);
            UI.showMessage(error.message || 'Произошла ошибка', 'error');
        }
    },

    /**
     * Initialize form event handlers
     */
    initFormHandlers() {
        // Category form
        document.getElementById('category-form').addEventListener('submit', async (e) => {
            e.preventDefault();

            const name = document.getElementById('category-name').value.trim();
            if (!name) {
                UI.showMessage('Введите название категории', 'error');
                return;
            }

            await this.handleFormSubmit('/categories/', { name }, e.target, 'Категория успешно добавлена!');
        });

        // Question form
        document.getElementById('question-form').addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = {
                category_id: document.getElementById('question-category').value,
                question_text: document.getElementById('question-text').value.trim(),
                answer_text: document.getElementById('answer-text').value.trim()
            };

            const validation = Utils.validateFormData(formData, ['category_id', 'question_text', 'answer_text']);

            if (!validation.isValid) {
                UI.showMessage('Заполните все поля', 'error');
                return;
            }

            // Convert category_id to integer
            formData.category_id = parseInt(formData.category_id);

            await this.handleFormSubmit('/questions/', formData, e.target, 'Вопрос успешно добавлен!');
        });
    }
};

// Global functions for backward compatibility
function switchTab(tabName, event) {
    UI.switchTab(tabName, event);

    // Load categories for form when switching to manage tab
    if (tabName === 'manage') {
        App.loadCategoriesForForm();
    }
}

function shuffleCards() {
    App.shuffleQuestions();
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

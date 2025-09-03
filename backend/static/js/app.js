const App = {
    allCategories: [],
    allQuestions: [],
    currentQuestions: [],
    currentPage: 1,

    async init() {
        UI.init();
        this.initEventListeners();
        await this.loadInitialData();
    },

    async loadInitialData() {
        UI.toggleLoading(true);
        try {
            const [cats, quests] = await Promise.all([API.categories.getAll(), API.questions.getAll()]);
            this.allCategories = cats;
            this.allQuestions = quests;
            this.currentQuestions = quests;

            UI.populateSelect(UI.elements.categorySelect, cats, 'Все вопросы');
            UI.populateSelect(UI.elements.questionCategorySelect, cats, 'Выберите категорию');
            UI.renderStats(cats.length, quests.length, this.currentPage);
            UI.renderQuestions(this.currentQuestions, 1);
            this.currentPage = 1;

            if (UI.elements.manageTab.classList.contains('active')) {
                UI.renderManagementList(this.allCategories, this.allQuestions);
            }
        } catch (e) {
            UI.elements.cardsContainer.innerHTML = `
                <div class="col-span-full text-center py-16">
                    <div class="text-6xl mb-4">❌</div>
                    <p class="text-red-400 text-xl mb-2">Ошибка загрузки данных</p>
                    <p class="text-gray-500">Убедитесь, что сервер запущен</p>
                </div>`;
        } finally {
            UI.toggleLoading(false);
        }
    },

    filterAndDisplayCards() {
        const catId = UI.elements.categorySelect.value;
        this.currentQuestions = catId
            ? this.allQuestions.filter(q => q.category_id == catId)
            : this.allQuestions;
        this.currentPage = 1;
        UI.renderQuestions(this.currentQuestions, 1);
        UI.renderStats(this.allCategories.length, this.allQuestions.length, this.currentPage);
    },

    shuffleQuestions() {
        this.currentQuestions = Utils.shuffleArray(this.currentQuestions);
        this.goToPage(1); // Go to first page after shuffling
    },

    goToPage(page) {
        this.currentPage = page;
        UI.renderQuestions(this.currentQuestions, page);
        UI.renderStats(this.allCategories.length, this.allQuestions.length, this.currentPage);
        window.scrollTo({ top: UI.elements.cardsContainer.offsetTop - 100, behavior: 'smooth' });
    },

    renderManagementList() {
        UI.renderManagementList(this.allCategories, this.allQuestions);
    },

    initEventListeners() {
        // Tabs
        UI.elements.studyTabBtn.addEventListener('click', (e) => UI.switchTab('study'));
        UI.elements.manageTabBtn.addEventListener('click', (e) => UI.switchTab('manage'));

        // Study Tab
        UI.elements.categorySelect.addEventListener('change', () => this.filterAndDisplayCards());
        UI.elements.shuffleBtn.addEventListener('click', () => this.shuffleQuestions());
        UI.elements.prevPageBtn.addEventListener('click', () => {
            if (this.currentPage > 1) this.goToPage(this.currentPage - 1);
        });
        UI.elements.nextPageBtn.addEventListener('click', () => {
            const totalPages = Math.ceil(this.currentQuestions.length / CONFIG.UI.CARDS_PER_PAGE);
            if (this.currentPage < totalPages) this.goToPage(this.currentPage + 1);
        });

        // Management Tab Forms
        UI.elements.categoryForm.addEventListener('submit', e => this.handleAddCategory(e));
        UI.elements.questionForm.addEventListener('submit', e => this.handleAddQuestion(e));

        // Modals Listeners (delegated to modals container)
        UI.elements.modalsContainer.addEventListener('click', (e) => {
            const target = e.target.closest('.modal-close-btn');
            if (target) {
                const modal = target.closest('.fixed');
                UI.closeModal(modal.id);
            }
            if (e.target.id === 'confirm-modal-no') {
                UI.closeModal('confirm-modal');
            }
        });

        // Edit Forms
        const editCategoryForm = UI.elements.modalsContainer.querySelector('#edit-category-form');
        const editQuestionForm = UI.elements.modalsContainer.querySelector('#edit-question-form');

        editCategoryForm.addEventListener('submit', e => this.handleEditCategory(e));
        editQuestionForm.addEventListener('submit', e => this.handleEditQuestion(e));
    },

    // --- Action Handlers ---
    async handleAddCategory(event) {
        event.preventDefault();
        const form = event.target;
        const name = form.querySelector('#category-name').value.trim();
        if (!name) return UI.showMessage('Название категории не может быть пустым.', 'error');

        try {
            await API.categories.create({ name });
            UI.showMessage('Категория успешно добавлена!', 'success');
            form.reset();
            await this.loadInitialData();
        } catch (error) {
            UI.showMessage(`Ошибка: ${error.message}`, 'error');
        }
    },

    async handleAddQuestion(event) {
        event.preventDefault();
        const form = event.target;
        const data = {
            category_id: parseInt(form.querySelector('#question-category').value),
            question_text: form.querySelector('#question-text').value.trim(),
            answer_text: form.querySelector('#answer-text').value.trim(),
        };

        if (!data.category_id || !data.question_text || !data.answer_text) {
            return UI.showMessage('Все поля должны быть заполнены.', 'error');
        }

        try {
            await API.questions.create(data);
            UI.showMessage('Вопрос успешно добавлен!', 'success');
            form.reset();
            await this.loadInitialData();
        } catch (error) {
            UI.showMessage(`Ошибка: ${error.message}`, 'error');
        }
    },

    async handleEditCategory(event) {
        event.preventDefault();
        const form = event.target;
        const id = parseInt(form.querySelector('#edit-category-id').value);
        const name = form.querySelector('#edit-category-name').value.trim();
        if (!name) return UI.showMessage('Название не может быть пустым.', 'error');

        try {
            await API.categories.update(id, { name });
            UI.showMessage('Категория успешно обновлена!', 'success');
            UI.closeModal('edit-category-modal');
            await this.loadInitialData();
        } catch (error) {
            UI.showMessage(`Ошибка: ${error.message}`, 'error');
        }
    },

    async handleEditQuestion(event) {
        event.preventDefault();
        const form = event.target;
        const id = parseInt(form.querySelector('#edit-question-id').value);
        const data = {
            category_id: parseInt(form.querySelector('#edit-question-category').value),
            question_text: form.querySelector('#edit-question-text').value.trim(),
            answer_text: form.querySelector('#edit-answer-text').value.trim(),
        };

        if (!data.category_id || !data.question_text || !data.answer_text) {
            return UI.showMessage('Все поля должны быть заполнены.', 'error');
        }

        try {
            await API.questions.update(id, data);
            UI.showMessage('Вопрос успешно обновлен!', 'success');
            UI.closeModal('edit-question-modal');
            await this.loadInitialData();
        } catch (error) {
            UI.showMessage(`Ошибка: ${error.message}`, 'error');
        }
    },

    openEditQuestionModal(questionId) {
        UI.openModal('edit-question-modal', { id: questionId });
    },

    handleDeleteCategory(id) {
        UI.openModal('confirm-modal', {
            message: 'Вы уверены, что хотите удалить эту категорию и все ее вопросы?',
            onConfirm: async () => {
                try {
                    await API.categories.delete(id);
                    UI.showMessage('Категория успешно удалена.', 'success');
                    await this.loadInitialData();
                } catch (error) {
                    UI.showMessage(`Ошибка: ${error.message}`, 'error');
                }
            }
        });
    },

    handleDeleteQuestion(id) {
        UI.openModal('confirm-modal', {
            message: 'Вы уверены, что хотите удалить этот вопрос?',
            onConfirm: async () => {
                try {
                    await API.questions.delete(id);
                    UI.showMessage('Вопрос успешно удален.', 'success');
                    await this.loadInitialData();
                } catch (error) {
                    UI.showMessage(`Ошибка: ${error.message}`, 'error');
                }
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

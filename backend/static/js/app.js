// App state
let appState = {
    categories: [],
    questions: [],
    filteredQuestions: [],
    selectedCategory: null,
    searchQuery: '',
    currentPage: 1,
    questionsPerPage: CONFIG.questionsPerPage,
    expandedCategories: new Set()
};

// Initialize app
document.addEventListener('DOMContentLoaded', function () {
    createGeometricShapes();
    loadData();
    setupEventListeners();
    setupDragAndDrop();
});

// Setup drag and drop for categories
function setupDragAndDrop() {
    new Sortable(document.getElementById('categories-container'), {
        animation: 150,
        ghostClass: 'sortable-placeholder',
        onStart: function (evt) {
            evt.item.classList.add('dragging');
        },
        onEnd: function (evt) {
            evt.item.classList.remove('dragging');
            console.log('New order:', Array.from(evt.to.children).map(el => el.dataset.id));
        }
    });
}

// Event listeners
function setupEventListeners() {
    document.getElementById('search-input').addEventListener('input', handleSearch);
    document.getElementById('category-form').addEventListener('submit', handleAddCategory);
    document.getElementById('question-form').addEventListener('submit', handleAddQuestion);
    document.getElementById('edit-form').addEventListener('submit', handleEdit);
}

// Select category filter
function selectCategory(categoryId) {
    appState.selectedCategory = appState.selectedCategory === categoryId ? null : categoryId;
    appState.currentPage = 1;
    filterQuestions();
    renderCategories();
    renderQuestions();
    updateStats();
}

// Handle search
function handleSearch(event) {
    appState.searchQuery = event.target.value.toLowerCase();
    appState.currentPage = 1;
    filterQuestions();
    renderQuestions();
    updateStats();
}

// Filter questions based on search and category
function filterQuestions() {
    appState.filteredQuestions = appState.questions.filter(question => {
        const matchesSearch = !appState.searchQuery ||
            question.question_text.toLowerCase().includes(appState.searchQuery) ||
            question.answer_text.toLowerCase().includes(appState.searchQuery);

        const matchesCategory = !appState.selectedCategory ||
            question.category_id === appState.selectedCategory;

        return matchesSearch && matchesCategory;
    });
}

// Go to specific page
function goToPage(page) {
    const totalPages = Math.ceil(appState.filteredQuestions.length / appState.questionsPerPage);
    if (page >= 1 && page <= totalPages && page !== appState.currentPage) {
        appState.currentPage = page;
        renderQuestions();
        updateStats();

        // Scroll to top of questions
        document.getElementById('questions-container').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Show answer modal
function showAnswer(questionId) {
    const question = appState.questions.find(q => q.id === questionId);
    if (!question) return;

    document.getElementById('modal-question').innerHTML = question.question_text;
    document.getElementById('modal-answer').innerHTML = formatAnswer(question.answer_text);
    showModal('answer-modal');
}

// Add category
async function handleAddCategory(event) {
    event.preventDefault();
    const name = document.getElementById('category-name').value.trim();

    if (!name) {
        showNotification('Введите название категории', 'warning');
        return;
    }

    // Check for duplicates
    if (appState.categories.some(c => c.name.toLowerCase() === name.toLowerCase())) {
        showNotification('Категория с таким названием уже существует', 'error');
        return;
    }

    try {
        await addCategoryAPI(name);
        showNotification('Категория добавлена', 'success');
        document.getElementById('category-form').reset();
        loadData();
    } catch (error) {
        showNotification('Ошибка добавления категории', 'error');
    }
}

// Add question
async function handleAddQuestion(event) {
    event.preventDefault();
    const categoryId = parseInt(document.getElementById('question-category').value);
    const questionText = document.getElementById('question-text').value.trim();
    const answerText = document.getElementById('answer-text').value.trim();

    if (!categoryId || !questionText || !answerText) {
        showNotification('Заполните все поля', 'warning');
        return;
    }

    // Check for duplicate questions
    if (appState.questions.some(q => q.question_text.toLowerCase() === questionText.toLowerCase())) {
        showNotification('Вопрос с таким текстом уже существует', 'error');
        return;
    }

    try {
        await addQuestionAPI(categoryId, questionText, answerText);
        showNotification('Вопрос добавлен', 'success');
        document.getElementById('question-form').reset();
        loadData();
    } catch (error) {
        showNotification('Ошибка добавления вопроса', 'error');
    }
}

// Edit category
function editCategory(categoryId) {
    const category = appState.categories.find(c => c.id === categoryId);
    if (!category) return;

    document.getElementById('edit-id').value = categoryId;
    document.getElementById('edit-type').value = 'category';
    document.getElementById('edit-fields').innerHTML = `
        <div class="form-group">
            <label class="form-label">Название категории</label>
            <input type="text" class="form-input" id="edit-name" value="${category.name}" required>
        </div>
    `;
    showModal('edit-modal');
}

// Edit question
function editQuestion(questionId) {
    const question = appState.questions.find(q => q.id === questionId);
    if (!question) return;

    document.getElementById('edit-id').value = questionId;
    document.getElementById('edit-type').value = 'question';

    const categoriesOptions = appState.categories.map(c =>
        `<option value="${c.id}" ${c.id === question.category_id ? 'selected' : ''}>${c.name}</option>`
    ).join('');

    document.getElementById('edit-fields').innerHTML = `
        <div class="form-group">
            <label class="form-label">Категория</label>
            <select class="form-select" id="edit-category" required>
                ${categoriesOptions}
            </select>
        </div>
        <div class="form-group">
            <label class="form-label">Вопрос</label>
            <textarea class="form-textarea" id="edit-question-text" required>${question.question_text}</textarea>
        </div>
        <div class="form-group">
            <label class="form-label">Ответ</label>
            <textarea class="form-textarea" id="edit-answer-text" required style="min-height: 150px;">${question.answer_text}</textarea>
        </div>
    `;
    showModal('edit-modal');
}

// Handle edit form submission
async function handleEdit(event) {
    event.preventDefault();
    const id = parseInt(document.getElementById('edit-id').value);
    const type = document.getElementById('edit-type').value;

    try {
        if (type === 'category') {
            const name = document.getElementById('edit-name').value.trim();

            // Check for duplicates (excluding current)
            if (appState.categories.some(c => c.id !== id && c.name.toLowerCase() === name.toLowerCase())) {
                showNotification('Категория с таким названием уже существует', 'error');
                return;
            }

            await updateCategoryAPI(id, name);
            showNotification('Категория обновлена', 'success');
            closeModal('edit-modal');
            loadData();
        } else if (type === 'question') {
            const categoryId = parseInt(document.getElementById('edit-category').value);
            const questionText = document.getElementById('edit-question-text').value.trim();
            const answerText = document.getElementById('edit-answer-text').value.trim();

            // Check for duplicate questions (excluding current)
            if (appState.questions.some(q => q.id !== id && q.question_text.toLowerCase() === questionText.toLowerCase())) {
                showNotification('Вопрос с таким текстом уже существует', 'error');
                return;
            }

            await updateQuestionAPI(id, categoryId, questionText, answerText);
            showNotification('Вопрос обновлен', 'success');
            closeModal('edit-modal');
            loadData();
        }
    } catch (error) {
        showNotification('Ошибка сохранения', 'error');
    }
}

// Delete category
async function deleteCategory(categoryId) {
    if (!confirm('Удалить категорию и все её вопросы?')) return;

    try {
        await deleteCategoryAPI(categoryId);
        showNotification('Категория удалена', 'success');
        if (appState.selectedCategory === categoryId) {
            appState.selectedCategory = null;
        }
        loadData();
    } catch (error) {
        showNotification('Ошибка удаления', 'error');
    }
}

// Delete question
async function deleteQuestion(questionId) {
    if (!confirm('Удалить вопрос?')) return;

    try {
        await deleteQuestionAPI(questionId);
        showNotification('Вопрос удален', 'success');
        loadData();
    } catch (error) {
        showNotification('Ошибка удаления', 'error');
    }
}

// Toggle category expansion in management
function toggleCategoryQuestions(categoryId) {
    if (appState.expandedCategories.has(categoryId)) {
        appState.expandedCategories.delete(categoryId);
    } else {
        appState.expandedCategories.add(categoryId);
    }
    renderManagement();
}

// Show all questions (clear filters)
function showAllQuestions() {
    appState.selectedCategory = null;
    appState.searchQuery = '';
    document.getElementById('search-input').value = '';
    appState.currentPage = 1;
    filterQuestions();
    renderCategories();
    renderQuestions();
    updateStats();
    showNotification('Показаны все вопросы', 'success');
}

// Shuffle questions
function shuffleQuestions() {
    appState.filteredQuestions = shuffleArray([...appState.filteredQuestions]);
    appState.currentPage = 1;
    renderQuestions();
    updateStats();
    showNotification('Вопросы перемешаны', 'success');
}

// Close modals when clicking outside
window.onclick = function (event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

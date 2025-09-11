// Load data from API
async function loadData() {
    try {
        showLoading();
        const [categoriesResponse, questionsResponse] = await Promise.all([
            fetch(`${API_BASE}/categories/`),
            fetch(`${API_BASE}/questions/`)
        ]);

        appState.categories = await categoriesResponse.json();
        appState.questions = await questionsResponse.json();

        // Sort categories alphabetically
        appState.categories.sort((a, b) => a.name.localeCompare(b.name, 'ru'));
        appState.filteredQuestions = [...appState.questions];

        renderCategories();
        renderQuestions();
        renderManagement();
        updateStats();
        populateSelects();

    } catch (error) {
        showNotification('Ошибка загрузки данных', 'error');
        console.error('Load error:', error);
    }
}

// Add category
async function addCategoryAPI(name) {
    const response = await fetch(`${API_BASE}/categories/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });

    if (!response.ok) {
        throw new Error('Ошибка сервера');
    }

    return response.json();
}

// Update category
async function updateCategoryAPI(id, name) {
    const response = await fetch(`${API_BASE}/categories/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });

    if (!response.ok) {
        throw new Error('Ошибка сервера');
    }

    return response.json();
}

// Delete category
async function deleteCategoryAPI(id) {
    const response = await fetch(`${API_BASE}/categories/${id}`, {
        method: 'DELETE'
    });

    if (!response.ok) {
        throw new Error('Ошибка сервера');
    }
}

// Add question
async function addQuestionAPI(categoryId, questionText, answerText) {
    const response = await fetch(`${API_BASE}/questions/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            category_id: categoryId,
            question_text: questionText,
            answer_text: answerText
        })
    });

    if (!response.ok) {
        throw new Error('Ошибка сервера');
    }

    return response.json();
}

// Update question
async function updateQuestionAPI(id, categoryId, questionText, answerText) {
    const response = await fetch(`${API_BASE}/questions/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            category_id: categoryId,
            question_text: questionText,
            answer_text: answerText
        })
    });

    if (!response.ok) {
        throw new Error('Ошибка сервера');
    }

    return response.json();
}

// Delete question
async function deleteQuestionAPI(id) {
    const response = await fetch(`${API_BASE}/questions/${id}`, {
        method: 'DELETE'
    });

    if (!response.ok) {
        throw new Error('Ошибка сервера');
    }
}

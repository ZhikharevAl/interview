// Show loading state
function showLoading() {
    document.getElementById('categories-container').innerHTML = '<div class="loading"></div>';
    document.getElementById('questions-container').innerHTML = '<div class="loading"></div>';
}

// Show modal
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Switch tabs
function switchTab(tabName) {
    const studyTab = document.getElementById('study-tab');
    const manageTab = document.getElementById('manage-tab');
    const tabButtons = document.querySelectorAll('.tab-btn');

    tabButtons.forEach(btn => btn.classList.remove('active'));

    if (tabName === 'study') {
        studyTab.style.display = 'block';
        manageTab.style.display = 'none';
        tabButtons[0].classList.add('active');
    } else {
        studyTab.style.display = 'none';
        manageTab.style.display = 'block';
        tabButtons[1].classList.add('active');
        renderManagement();
    }
}

// Render categories
function renderCategories() {
    const container = document.getElementById('categories-container');

    if (appState.categories.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📁</span>
                <div>Нет категорий</div>
                <div style="font-size: 12px; margin-top: 10px;">Создайте первую категорию во вкладке "Управление"</div>
            </div>
        `;
        return;
    }

    container.innerHTML = appState.categories.map(category => {
        const questionsCount = appState.questions.filter(q => q.category_id === category.id).length;
        const isSelected = appState.selectedCategory === category.id;

        return `
            <div class="category-card ${isSelected ? 'selected' : ''}"
                 data-id="${category.id}"
                 onclick="selectCategory(${category.id})">
                <div class="category-actions">
                    <button class="mini-btn edit" onclick="event.stopPropagation(); editCategory(${category.id})" title="Редактировать">✏</button>
                    <button class="mini-btn delete" onclick="event.stopPropagation(); deleteCategory(${category.id})" title="Удалить">×</button>
                </div>
                <div class="category-name">${category.name}</div>
                <div class="category-count">Вопросов - ${questionsCount}</div>
            </div>
        `;
    }).join('');
}

// Render questions
function renderQuestions() {
    const container = document.getElementById('questions-container');
    const paginationContainer = document.getElementById('pagination-container');

    if (appState.filteredQuestions.length === 0) {
        const message = appState.searchQuery || appState.selectedCategory
            ? 'Нет вопросов по вашему запросу'
            : 'Нет вопросов';

        container.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">❓</span>
                <div>${message}</div>
                <div style="font-size: 12px; margin-top: 10px;">Попробуйте изменить поиск или добавить новые вопросы</div>
            </div>
        `;
        paginationContainer.style.display = 'none';
        return;
    }

    const totalPages = Math.ceil(appState.filteredQuestions.length / appState.questionsPerPage);
    const startIndex = (appState.currentPage - 1) * appState.questionsPerPage;
    const endIndex = startIndex + appState.questionsPerPage;
    const paginatedQuestions = appState.filteredQuestions.slice(startIndex, endIndex);

    container.innerHTML = paginatedQuestions.map(question => {
        const category = appState.categories.find(c => c.id === question.category_id);
        const categoryName = category ? category.name : 'Неизвестная категория';

        return `
            <div class="question-card" onclick="showAnswer(${question.id})">
                <div class="question-text">${question.question_text}</div>
                <div class="question-meta">${categoryName}</div>
            </div>
        `;
    }).join('');

    // Render pagination if needed
    if (totalPages > 1) {
        renderPagination(totalPages);
        paginationContainer.style.display = 'flex';
    } else {
        paginationContainer.style.display = 'none';
    }
}

// Render pagination
function renderPagination(totalPages) {
    const container = document.getElementById('pagination-container');
    const current = appState.currentPage;

    let html = '';

    // Previous button
    html += `
        <button class="pagination-btn" onclick="goToPage(${current - 1})" ${current === 1 ? 'disabled' : ''}>
            ←
        </button>
    `;

    // Calculate page range
    let startPage = Math.max(1, current - Math.floor(CONFIG.maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + CONFIG.maxVisiblePages - 1);

    // Adjust start if we're near the end
    if (endPage - startPage < CONFIG.maxVisiblePages - 1) {
        startPage = Math.max(1, endPage - CONFIG.maxVisiblePages + 1);
    }

    // First page if not in range
    if (startPage > 1) {
        html += `<button class="pagination-btn" onclick="goToPage(1)">1</button>`;
        if (startPage > 2) {
            html += `<span class="pagination-info">...</span>`;
        }
    }

    // Page numbers
    for (let i = startPage; i <= endPage; i++) {
        html += `
            <button class="pagination-btn ${i === current ? 'active' : ''}" onclick="goToPage(${i})">
                ${i}
            </button>
        `;
    }

    // Last page if not in range
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            html += `<span class="pagination-info">...</span>`;
        }
        html += `<button class="pagination-btn" onclick="goToPage(${totalPages})">${totalPages}</button>`;
    }

    // Next button
    html += `
        <button class="pagination-btn" onclick="goToPage(${current + 1})" ${current === totalPages ? 'disabled' : ''}>
            →
        </button>
    `;

    // Info
    const startItem = (current - 1) * appState.questionsPerPage + 1;
    const endItem = Math.min(current * appState.questionsPerPage, appState.filteredQuestions.length);
    html += `
        <div class="pagination-info">
            ${startItem}-${endItem} из ${appState.filteredQuestions.length}
        </div>
    `;

    container.innerHTML = html;
}

// Render management list with collapsible categories
function renderManagement() {
    const container = document.getElementById('management-list');

    if (appState.categories.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📋</span>
                <div>Нет данных для управления</div>
            </div>
        `;
        return;
    }

    let html = '';

    appState.categories.forEach(category => {
        const questionsCount = appState.questions.filter(q => q.category_id === category.id).length;
        const isExpanded = appState.expandedCategories.has(category.id);

        // Category header
        html += `
            <div class="category-header" onclick="toggleCategoryQuestions(${category.id})">
                <div>
                    <strong>${category.name}</strong>
                    <div style="font-size: 11px; opacity: 0.7;">${questionsCount} вопросов</div>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="management-actions">
                        <button class="mini-btn edit" onclick="event.stopPropagation(); editCategory(${category.id})" title="Редактировать">✏</button>
                        <button class="mini-btn delete" onclick="event.stopPropagation(); deleteCategory(${category.id})" title="Удалить">×</button>
                    </div>
                    <div class="category-toggle ${isExpanded ? 'expanded' : ''}">▶</div>
                </div>
            </div>
        `;

        // Category questions (collapsible)
        const categoryQuestions = appState.questions.filter(q => q.category_id === category.id);
        html += `<div class="category-questions ${isExpanded ? 'expanded' : ''}">`;

        categoryQuestions.forEach(question => {
            const truncatedText = question.question_text.length > 60
                ? question.question_text.substring(0, 60) + '...'
                : question.question_text;

            html += `
                <div class="question-item">
                    <div class="question-preview">${truncatedText}</div>
                    <div class="management-actions">
                        <button class="mini-btn edit" onclick="editQuestion(${question.id})" title="Редактировать">✏</button>
                        <button class="mini-btn delete" onclick="deleteQuestion(${question.id})" title="Удалить">×</button>
                    </div>
                </div>
            `;
        });

        html += '</div>';
    });

    container.innerHTML = html;
}

// Update stats
function updateStats() {
    document.getElementById('categories-count').textContent = appState.categories.length;
    document.getElementById('questions-count').textContent = appState.questions.length;

    // Calculate how many questions are currently shown on this page
    const startIndex = (appState.currentPage - 1) * appState.questionsPerPage;
    const endIndex = Math.min(startIndex + appState.questionsPerPage, appState.filteredQuestions.length);
    const shownCount = appState.filteredQuestions.length > 0 ? endIndex - startIndex : 0;

    document.getElementById('filtered-count').textContent = shownCount;
    document.getElementById('page-number').textContent = appState.currentPage;
}

// Populate select options
function populateSelects() {
    const select = document.getElementById('question-category');
    select.innerHTML = '<option value="">Выберите категорию</option>';

    appState.categories.forEach(category => {
        select.innerHTML += `<option value="${category.id}">${category.name}</option>`;
    });
}

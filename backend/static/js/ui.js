const UI = {
    elements: {},
    init() {
        this.elements = {
            // Tabs
            studyTabBtn: document.getElementById('study-tab-btn'),
            manageTabBtn: document.getElementById('manage-tab-btn'),
            studyTab: document.getElementById('study-tab'),
            manageTab: document.getElementById('manage-tab'),
            // Study Tab
            statsContainer: document.getElementById('stats-container'),
            categorySelect: document.getElementById('category-select'),
            shuffleBtn: document.getElementById('shuffle-btn'),
            loadingDiv: document.getElementById('loading'),
            cardsContainer: document.getElementById('cards-container'),
            paginationContainer: document.getElementById('pagination-container'),
            prevPageBtn: document.getElementById('prev-page'),
            nextPageBtn: document.getElementById('next-page'),
            pageNumbers: document.getElementById('page-numbers'),
            // Management Tab
            messageContainer: document.getElementById('message-container'),
            categoryForm: document.getElementById('category-form'),
            questionForm: document.getElementById('question-form'),
            questionCategorySelect: document.getElementById('question-category'),
            managementList: document.getElementById('management-list'),
            // Modals
            modalsContainer: document.getElementById('modals-container'),
        };
        this.renderAllModals();
        // Re-assign modal elements after rendering
        this.elements.answerModal = document.getElementById('answer-modal');
        this.elements.editCategoryModal = document.getElementById('edit-category-modal');
        this.elements.editQuestionModal = document.getElementById('edit-question-modal');
        this.elements.confirmModal = document.getElementById('confirm-modal');
    },

    switchTab(tabName) {
        const isStudy = tabName === 'study';
        this.elements.studyTab.classList.toggle('active', isStudy);
        this.elements.manageTab.classList.toggle('active', !isStudy);
        this.elements.studyTabBtn.classList.toggle('active', isStudy);
        this.elements.manageTabBtn.classList.toggle('active', !isStudy);

        if (!isStudy) {
            App.renderManagementList();
        }
    },

    toggleLoading: (show) => {
        UI.elements.loadingDiv.classList.toggle('hidden', !show);
        if (show) {
            UI.elements.loadingDiv.innerHTML = `
                <div class="inline-flex items-center space-x-2">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                    <span>Загружаем вопросы...</span>
                </div>`;
        }
    },

    showMessage(text, type = 'success') {
        const styles = type === 'success'
            ? 'bg-green-900 bg-opacity-50 border-green-500 text-green-300'
            : 'bg-red-900 bg-opacity-50 border-red-500 text-red-300';

        this.elements.messageContainer.innerHTML = `
            <div class="border ${styles} px-6 py-4 rounded-xl shadow-lg slide-in backdrop-blur-lg" role="alert">
                <div class="flex items-center"><span class="font-medium">${text}</span></div>
            </div>`;
        setTimeout(() => { this.elements.messageContainer.innerHTML = ''; }, CONFIG.UI.MESSAGE_TIMEOUT);
    },

    populateSelect(selectElement, options, defaultText = '') {
        selectElement.innerHTML = defaultText ? `<option value="">${defaultText}</option>` : '';
        options.forEach(option => selectElement.add(new Option(option.name, option.id)));
    },

    renderStats(categoriesCount, questionsCount, currentPage) {
        this.elements.statsContainer.innerHTML = `
            <div class="glass rounded-xl p-6 text-center fade-in-card">
                <div class="text-3xl mb-2 text-blue-400">📁</div>
                <div class="text-3xl font-bold text-blue-400">${categoriesCount}</div>
                <div class="text-sm font-medium text-gray-400 mt-1">Категорий</div>
            </div>
            <div class="glass rounded-xl p-6 text-center fade-in-card" style="animation-delay: 100ms">
                <div class="text-3xl mb-2 text-blue-400">❓</div>
                <div class="text-3xl font-bold text-blue-400">${questionsCount}</div>
                <div class="text-sm font-medium text-gray-400 mt-1">Всего вопросов</div>
            </div>
            <div class="glass rounded-xl p-6 text-center fade-in-card" style="animation-delay: 200ms">
                <div class="text-3xl mb-2 text-green-400">📊</div>
                <div class="text-3xl font-bold text-green-400">${Math.round(questionsCount / Math.max(categoriesCount, 1)) || 0}</div>
                <div class="text-sm font-medium text-gray-400 mt-1">В среднем</div>
            </div>
            <div class="glass rounded-xl p-6 text-center fade-in-card" style="animation-delay: 300ms">
                <div class="text-3xl mb-2 text-purple-400">🎯</div>
                <div class="text-3xl font-bold text-purple-400">${currentPage || 1}</div>
                <div class="text-sm font-medium text-gray-400 mt-1">Страница</div>
            </div>`;
    },

    renderQuestions(questions, page = 1) {
        const container = this.elements.cardsContainer;
        container.innerHTML = '';

        if (questions.length === 0) {
            container.innerHTML = `
                <div class="col-span-full flex flex-col items-center justify-center py-16 text-gray-400">
                    <div class="text-6xl mb-4">🤔</div>
                    <p class="text-xl mb-2 text-gray-300">В этой категории пока нет вопросов</p>
                    <p class="text-sm">Добавьте их во вкладке "Управление"!</p>
                </div>`;
            this.elements.paginationContainer.classList.add('hidden');
            return;
        }

        const itemsPerPage = CONFIG.UI.CARDS_PER_PAGE;
        const startIndex = (page - 1) * itemsPerPage;
        const paginatedQuestions = questions.slice(startIndex, startIndex + itemsPerPage);

        // A single, simple grid for all cards on the page
        container.className = 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mb-8';

        paginatedQuestions.forEach((q, i) => {
            container.insertAdjacentHTML('beforeend', this.createQuestionCard(q, i));
        });


        // Re-bind click events after rendering
        container.querySelectorAll('.question-card').forEach((card, i) => {
            const question = paginatedQuestions[i];
            if (question) {
                const fQuestion = Utils.formatText(question.question_text);
                const fAnswer = Utils.formatText(question.answer_text);
                card.onclick = () => this.openModal('answer-modal', { question: fQuestion, answer: fAnswer });
            }
        });

        this.renderPagination(questions.length, page, itemsPerPage);
    },


    createQuestionCard(question, index) {
        const fQuestion = Utils.formatText(question.question_text);
        return `
            <div class="fade-in-card question-card backdrop-blur-sm p-6 rounded-xl shadow-lg cursor-pointer" style="min-height: 220px; animation-delay: ${index * CONFIG.UI.ANIMATION_DELAY}ms;">
                <div class="flex items-center justify-center h-full text-center">
                    <div class="text-lg font-semibold text-gray-200 line-clamp-4">${fQuestion}</div>
                </div>
            </div>`;
    },

    renderPagination(totalItems, currentPage, itemsPerPage) {
        const totalPages = Math.ceil(totalItems / itemsPerPage);

        if (totalPages <= 1) {
            this.elements.paginationContainer.classList.add('hidden');
            return;
        }
        this.elements.paginationContainer.classList.remove('hidden');

        this.elements.prevPageBtn.disabled = currentPage === 1;
        this.elements.nextPageBtn.disabled = currentPage === totalPages;

        this.elements.pageNumbers.innerHTML = '';

        const createButton = (page, isActive = false) => {
            const button = document.createElement('button');
            button.className = `pagination-button px-4 py-2 rounded-lg shadow-md font-medium transition-all ${isActive ? 'active' : ''}`;
            button.textContent = page;
            button.onclick = () => App.goToPage(page);
            return button;
        };

        const createEllipsis = () => {
            const span = document.createElement('span');
            span.className = 'px-2 py-2 text-gray-500';
            span.textContent = '...';
            return span;
        };

        if (totalPages <= 5) {
            for (let i = 1; i <= totalPages; i++) {
                this.elements.pageNumbers.appendChild(createButton(i, i === currentPage));
            }
        } else {
            if (currentPage > 2) {
                this.elements.pageNumbers.appendChild(createButton(1));
                if (currentPage > 3) {
                    this.elements.pageNumbers.appendChild(createEllipsis());
                }
            }

            for (let i = Math.max(1, currentPage - 1); i <= Math.min(totalPages, currentPage + 1); i++) {
                this.elements.pageNumbers.appendChild(createButton(i, i === currentPage));
            }

            if (currentPage < totalPages - 1) {
                if (currentPage < totalPages - 2) {
                    this.elements.pageNumbers.appendChild(createEllipsis());
                }
                this.elements.pageNumbers.appendChild(createButton(totalPages));
            }
        }
    },

    renderManagementList(categories, questions) {
        const container = this.elements.managementList;
        container.innerHTML = '';
        if (categories.length === 0) {
            container.innerHTML = `
                <div class="text-center text-gray-400 py-8"><div class="text-4xl mb-4">📁</div><p>Категории еще не созданы.</p></div>`;
            return;
        }
        categories.forEach((cat, index) => {
            const catQuestions = questions.filter(q => q.category_id === cat.id);
            container.insertAdjacentHTML('beforeend', this.createManagementListItem(cat, catQuestions, index));
        });
    },

    createManagementListItem(category, questions, index) {
        const hasQuestions = questions.length > 0;
        const questionsHtml = hasQuestions
            ? `<div class="mt-4">
                 <div class="question-list" id="questions-${category.id}">
                   ${questions.map(q => `
                     <div class="flex justify-between items-start py-3 px-4 bg-slate-800 bg-opacity-50 rounded-lg mb-2 border border-blue-500 border-opacity-20">
                       <div class="flex-1 mr-4">
                         <p class="text-sm text-gray-300 font-medium line-clamp-2">${q.question_text}</p>
                       </div>
                       <div class="flex space-x-1">
                         <button onclick="App.openEditQuestionModal(${q.id})" class="text-blue-400 hover:text-blue-300 hover:bg-blue-900 hover:bg-opacity-30 p-2 rounded-lg transition-colors" title="Редактировать вопрос">✏️</button>
                         <button onclick="App.handleDeleteQuestion(${q.id})" class="text-red-400 hover:text-red-300 hover:bg-red-900 hover:bg-opacity-30 p-2 rounded-lg transition-colors" title="Удалить вопрос">🗑️</button>
                       </div>
                     </div>
                   `).join('')}
                 </div>
               </div>`
            : '<div class="mt-4 text-sm text-gray-500 italic">Нет вопросов в этой категории</div>';

        return `
            <div class="management-item p-6 rounded-xl fade-in-card" style="animation-delay: ${index * 100}ms">
                <div class="flex justify-between items-center cursor-pointer" onclick="UI.toggleQuestionsVisibility(${category.id})">
                    <div class="flex items-center space-x-3">
                        <div class="text-2xl">📚</div>
                        <div>
                            <h4 class="text-lg font-semibold text-gray-200">${category.name}</h4>
                            <p class="text-sm text-gray-400">${questions.length} ${questions.length === 1 ? 'вопрос' : questions.length < 5 ? 'вопроса' : 'вопросов'}</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button onclick="event.stopPropagation(); UI.openModal('edit-category-modal', {id: ${category.id}, name: '${category.name}'})" class="p-3 hover:bg-blue-900 hover:bg-opacity-30 rounded-lg transition-colors text-blue-400" title="Редактировать">✏️</button>
                        <button onclick="event.stopPropagation(); App.handleDeleteCategory(${category.id})" class="p-3 hover:bg-red-900 hover:bg-opacity-30 rounded-lg transition-colors text-red-400" title="Удалить категорию">🗑️</button>
                    </div>
                </div>
                ${questionsHtml}
            </div>`;
    },

    toggleQuestionsVisibility(categoryId) {
        const list = document.getElementById(`questions-${categoryId}`);
        if (list) {
            list.classList.toggle('expanded');
        }
    },

    openModal(modalId, data = {}) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        if (modalId === 'answer-modal') {
            modal.querySelector('#modal-question').innerHTML = data.question;
            modal.querySelector('#modal-answer').innerHTML = data.answer;
        } else if (modalId === 'edit-category-modal') {
            modal.querySelector('#edit-category-id').value = data.id;
            modal.querySelector('#edit-category-name').value = data.name;
        } else if (modalId === 'edit-question-modal') {
            const question = App.allQuestions.find(q => q.id === data.id);
            if (!question) return;
            const categorySelect = modal.querySelector('#edit-question-category');
            this.populateSelect(categorySelect, App.allCategories, '');
            categorySelect.value = question.category_id;
            modal.querySelector('#edit-question-id').value = data.id;
            modal.querySelector('#edit-question-text').value = question.question_text;
            modal.querySelector('#edit-answer-text').value = question.answer_text;
        } else if (modalId === 'confirm-modal') {
            modal.querySelector('#confirm-modal-text').textContent = data.message;
            const yesButton = modal.querySelector('#confirm-modal-yes');
            const newYesButton = yesButton.cloneNode(true);
            yesButton.parentNode.replaceChild(newYesButton, yesButton);
            newYesButton.onclick = () => {
                this.closeModal(modalId);
                data.onConfirm();
            };
        }
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    },

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    },

    renderAllModals() {
        this.elements.modalsContainer.innerHTML = `
            <!-- Answer Modal -->
            <div id="answer-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black bg-opacity-80 p-4 transition-all duration-300">
                <div class="relative w-full max-w-4xl max-h-[90vh] glass-light rounded-2xl shadow-2xl flex flex-col overflow-hidden">
                    <div class="flex items-start justify-between p-6 border-b border-blue-500 border-opacity-30">
                        <div id="modal-question" class="text-xl font-semibold text-gray-200 leading-relaxed flex-1 mr-4"></div>
                        <button type="button" class="modal-close-btn text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg p-2 transition-colors">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                    <div id="modal-answer" class="p-6 overflow-y-auto text-gray-300 leading-relaxed custom-scrollbar flex-1"></div>
                </div>
            </div>

            <!-- Edit Category Modal -->
            <div id="edit-category-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black bg-opacity-80 p-4">
                 <div class="relative w-full max-w-md glass-light rounded-xl shadow-2xl">
                    <div class="flex items-center justify-between p-6 border-b border-blue-500 border-opacity-30">
                        <h3 class="text-xl font-semibold text-gray-200">Редактировать категорию</h3>
                        <button type="button" class="modal-close-btn text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg p-2 transition-colors">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                    <form id="edit-category-form" class="p-6">
                        <input type="hidden" id="edit-category-id">
                        <div class="mb-4">
                            <label for="edit-category-name" class="block mb-2 text-sm font-medium text-gray-300">Новое название</label>
                            <input type="text" id="edit-category-name" required class="w-full form-input rounded-lg p-3">
                        </div>
                        <button type="submit" class="w-full btn-primary font-medium rounded-lg px-5 py-3 transition-all">Сохранить</button>
                    </form>
                </div>
            </div>

            <!-- Edit Question Modal -->
            <div id="edit-question-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black bg-opacity-80 p-4">
                <div class="relative w-full max-w-2xl glass-light rounded-xl shadow-2xl">
                    <div class="flex items-center justify-between p-6 border-b border-blue-500 border-opacity-30">
                        <h3 class="text-xl font-semibold text-gray-200">Редактировать вопрос</h3>
                        <button type="button" class="modal-close-btn text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg p-2 transition-colors">
                           <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                    <form id="edit-question-form" class="p-6 space-y-4">
                        <input type="hidden" id="edit-question-id">
                        <div>
                            <label for="edit-question-category" class="block mb-2 text-sm font-medium text-gray-300">Категория</label>
                            <select id="edit-question-category" required class="w-full form-input rounded-lg p-3"></select>
                        </div>
                        <div>
                            <label for="edit-question-text" class="block mb-2 text-sm font-medium text-gray-300">Вопрос</label>
                            <textarea id="edit-question-text" rows="3" required class="w-full form-input rounded-lg p-3 resize-none"></textarea>
                        </div>
                        <div>
                            <label for="edit-answer-text" class="block mb-2 text-sm font-medium text-gray-300">Ответ</label>
                            <textarea id="edit-answer-text" rows="6" required class="w-full form-input rounded-lg p-3 resize-none"></textarea>
                        </div>
                        <button type="submit" class="w-full btn-primary font-medium rounded-lg px-5 py-3 transition-all">Сохранить</button>
                    </form>
                </div>
            </div>

            <!-- Confirmation Modal -->
            <div id="confirm-modal" class="fixed inset-0 z-[100] hidden items-center justify-center bg-black bg-opacity-80 p-4">
                <div class="relative w-full max-w-md glass-light rounded-xl shadow-2xl">
                    <div class="p-6 text-center">
                        <div class="mx-auto mb-4 h-12 w-12 text-orange-500 text-4xl">⚠️</div>
                        <h3 id="confirm-modal-text" class="mb-5 text-lg font-normal text-gray-300">Вы уверены?</h3>
                        <div class="flex space-x-4">
                            <button id="confirm-modal-yes" class="flex-1 btn-danger font-medium rounded-lg px-5 py-3 transition-all">Да, удалить</button>
                            <button id="confirm-modal-no" class="flex-1 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg border border-gray-600 font-medium px-5 py-3 transition-all">Отменить</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
};

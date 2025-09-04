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

        // Добавляем анимацию переключения
        const currentTab = isStudy ? this.elements.manageTab : this.elements.studyTab;
        const newTab = isStudy ? this.elements.studyTab : this.elements.manageTab;

        // Скрываем текущую вкладку с анимацией
        currentTab.style.transform = 'translateX(-20px)';
        currentTab.style.opacity = '0';

        setTimeout(() => {
            this.elements.studyTab.classList.toggle('active', isStudy);
            this.elements.manageTab.classList.toggle('active', !isStudy);
            this.elements.studyTabBtn.classList.toggle('active', isStudy);
            this.elements.manageTabBtn.classList.toggle('active', !isStudy);

            // Показываем новую вкладку с анимацией
            newTab.style.transform = 'translateX(0)';
            newTab.style.opacity = '1';
        }, 150);

        if (!isStudy) {
            setTimeout(() => {
                App.renderManagementList();
            }, 200);
        }
    },

    toggleLoading: (show) => {
        UI.elements.loadingDiv.classList.toggle('hidden', !show);
        if (show) {
            UI.elements.loadingDiv.innerHTML = `
                <div class="inline-flex items-center space-x-3">
                    <div class="relative">
                        <div class="animate-spin rounded-full h-8 w-8 border-2 border-blue-500 border-t-transparent"></div>
                        <div class="absolute inset-1 animate-pulse rounded-full bg-blue-500/20"></div>
                    </div>
                    <span class="text-lg font-medium">Загружаем вопросы...</span>
                    <div class="flex space-x-1">
                        <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0s"></div>
                        <div class="w-2 h-2 bg-green-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                        <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    </div>
                </div>`;
        }
    },

    showMessage(text, type = 'success') {
        const isSuccess = type === 'success';
        const styles = isSuccess
            ? 'bg-gradient-to-r from-green-900/80 to-emerald-900/60 border-green-500/50 text-green-200'
            : 'bg-gradient-to-r from-red-900/80 to-rose-900/60 border-red-500/50 text-red-200';

        const icon = isSuccess ? '✅' : '❌';

        this.elements.messageContainer.innerHTML = `
            <div class="border ${styles} px-6 py-4 rounded-xl shadow-lg slide-in backdrop-blur-lg relative overflow-hidden" role="alert">
                <div class="absolute inset-0 bg-gradient-to-r ${isSuccess ? 'from-green-500/10 to-transparent' : 'from-red-500/10 to-transparent'}"></div>
                <div class="flex items-center gap-3 relative z-10">
                    <span class="text-xl">${icon}</span>
                    <span class="font-medium">${text}</span>
                </div>
                <div class="absolute bottom-0 left-0 h-1 bg-gradient-to-r ${isSuccess ? 'from-green-500 to-emerald-400' : 'from-red-500 to-rose-400'} animate-pulse"></div>
            </div>`;

        setTimeout(() => {
            const message = this.elements.messageContainer.firstElementChild;
            if (message) {
                message.style.transform = 'translateY(-100%)';
                message.style.opacity = '0';
                setTimeout(() => {
                    this.elements.messageContainer.innerHTML = '';
                }, 300);
            }
        }, CONFIG.UI.MESSAGE_TIMEOUT);
    },

    populateSelect(selectElement, options, defaultText = '') {
        selectElement.innerHTML = defaultText ? `<option value="">${defaultText}</option>` : '';
        options.forEach(option => {
            const optionElement = new Option(option.name, option.id);
            selectElement.add(optionElement);
        });
    },

    renderStats(categoriesCount, questionsCount, currentPage) {
        const stats = [
            { icon: '📁', value: categoriesCount, label: 'Категорий', color: 'blue' },
            { icon: '❓', value: questionsCount, label: 'Всего вопросов', color: 'emerald' },
            { icon: '📊', value: Math.round(questionsCount / Math.max(categoriesCount, 1)) || 0, label: 'В среднем', color: 'purple' },
            { icon: '🎯', value: currentPage || 1, label: 'Страница', color: 'orange' }
        ];

        const colorClasses = {
            blue: 'text-blue-400',
            emerald: 'text-emerald-400',
            purple: 'text-purple-400',
            orange: 'text-orange-400'
        };

        this.elements.statsContainer.innerHTML = stats.map((stat, index) => `
            <div class="glass rounded-xl p-6 text-center fade-in-card hover:scale-105 transition-transform duration-300" style="animation-delay: ${index * 100}ms">
                <div class="text-3xl mb-2 ${colorClasses[stat.color]} animate-pulse">${stat.icon}</div>
                <div class="text-3xl font-bold ${colorClasses[stat.color]} counter" data-target="${stat.value}">0</div>
                <div class="text-sm font-medium text-gray-400 mt-1">${stat.label}</div>
                <div class="mt-2 h-1 bg-gray-700 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r ${this.getGradientClass(stat.color)} rounded-full transform -translate-x-full animate-slide-in" style="animation-delay: ${(index * 100) + 500}ms"></div>
                </div>
            </div>
        `).join('');

        // Анимация счетчиков
        setTimeout(() => {
            this.animateCounters();
        }, 300);
    },

    getGradientClass(color) {
        const gradients = {
            blue: 'from-blue-500 to-blue-400',
            emerald: 'from-emerald-500 to-emerald-400',
            purple: 'from-purple-500 to-purple-400',
            orange: 'from-orange-500 to-orange-400'
        };
        return gradients[color] || 'from-gray-500 to-gray-400';
    },

    animateCounters() {
        const counters = document.querySelectorAll('.counter');
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            let current = 0;
            const increment = target / 30;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                counter.textContent = Math.floor(current);
            }, 50);
        });
    },

    renderQuestions(questions, page = 1) {
        const container = this.elements.cardsContainer;
        container.innerHTML = '';

        if (questions.length === 0) {
            container.innerHTML = `
                <div class="col-span-full flex flex-col items-center justify-center py-16 text-gray-400">
                    <div class="text-8xl mb-6 animate-bounce">🤔</div>
                    <p class="text-2xl mb-3 text-gray-300 font-semibold">В этой категории пока нет вопросов</p>
                    <p class="text-lg text-gray-500">Добавьте их во вкладке "Управление"!</p>
                    <div class="mt-6">
                        <div class="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/20 rounded-full text-blue-300 text-sm">
                            <span class="animate-pulse">💡</span>
                            Совет: Начните с создания категории
                        </div>
                    </div>
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
        const colors = ['from-blue-500/10 to-purple-500/5', 'from-emerald-500/10 to-blue-500/5', 'from-purple-500/10 to-pink-500/5', 'from-orange-500/10 to-red-500/5'];
        const randomColor = colors[index % colors.length];

        return `
            <div class="fade-in-card question-card backdrop-blur-sm p-6 rounded-xl shadow-lg cursor-pointer group relative overflow-hidden"
                 style="min-height: 220px; animation-delay: ${index * CONFIG.UI.ANIMATION_DELAY}ms;">
                <div class="absolute inset-0 bg-gradient-to-br ${randomColor} opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div class="relative z-10 flex items-center justify-center h-full text-center">
                    <div class="space-y-3">
                        <div class="text-2xl group-hover:scale-110 transition-transform duration-300">💭</div>
                        <div class="text-lg font-semibold text-gray-200 line-clamp-4 group-hover:text-white transition-colors duration-300">
                            ${fQuestion}
                        </div>
                        <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-sm text-gray-400">
                            Нажмите для просмотра ответа
                        </div>
                    </div>
                </div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 to-purple-500 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
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

        // Добавляем стили для disabled кнопок
        this.elements.prevPageBtn.classList.toggle('opacity-50', currentPage === 1);
        this.elements.nextPageBtn.classList.toggle('opacity-50', currentPage === totalPages);

        this.elements.pageNumbers.innerHTML = '';

        const createButton = (page, isActive = false) => {
            const button = document.createElement('button');
            button.className = `pagination-button px-4 py-2 rounded-lg shadow-md font-medium transition-all transform hover:scale-105 ${isActive ? 'active scale-105' : ''}`;
            button.textContent = page;
            button.onclick = () => App.goToPage(page);
            return button;
        };

        const createEllipsis = () => {
            const span = document.createElement('span');
            span.className = 'px-2 py-2 text-gray-500 animate-pulse';
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
                <div class="text-center text-gray-400 py-12">
                    <div class="text-6xl mb-6 animate-bounce">📁</div>
                    <p class="text-xl mb-3">Категории еще не созданы.</p>
                    <p class="text-gray-500">Создайте первую категорию выше ☝️</p>
                </div>`;
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
                     <div class="flex justify-between items-start py-3 px-4 bg-slate-800 bg-opacity-50 rounded-lg mb-2 border border-blue-500 border-opacity-20 hover:border-opacity-40 transition-all duration-300 hover:bg-slate-700 hover:bg-opacity-50">
                       <div class="flex-1 mr-4">
                         <p class="text-sm text-gray-300 font-medium line-clamp-2 hover:text-white transition-colors">${q.question_text}</p>
                       </div>
                       <div class="flex space-x-1">
                         <button onclick="App.openEditQuestionModal(${q.id})" class="text-blue-400 hover:text-blue-300 hover:bg-blue-900 hover:bg-opacity-30 p-2 rounded-lg transition-all duration-300 transform hover:scale-110" title="Редактировать вопрос">✏️</button>
                         <button onclick="App.handleDeleteQuestion(${q.id})" class="text-red-400 hover:text-red-300 hover:bg-red-900 hover:bg-opacity-30 p-2 rounded-lg transition-all duration-300 transform hover:scale-110" title="Удалить вопрос">🗑️</button>
                       </div>
                     </div>
                   `).join('')}
                 </div>
               </div>`
            : '<div class="mt-4 text-sm text-gray-500 italic flex items-center gap-2"><span>💭</span>Нет вопросов в этой категории</div>';

        return `
            <div class="management-item p-6 rounded-xl fade-in-card hover:scale-[1.02] transition-all duration-300" style="animation-delay: ${index * 100}ms">
                <div class="flex justify-between items-center cursor-pointer" onclick="UI.toggleQuestionsVisibility(${category.id})">
                    <div class="flex items-center space-x-3">
                        <div class="text-2xl animate-pulse">📚</div>
                        <div>
                            <h4 class="text-lg font-semibold text-gray-200 hover:text-white transition-colors">${category.name}</h4>
                            <p class="text-sm text-gray-400">
                                ${questions.length} ${questions.length === 1 ? 'вопрос' : questions.length < 5 ? 'вопроса' : 'вопросов'}
                                ${hasQuestions ? '<span class="ml-2 text-green-400">✓</span>' : '<span class="ml-2 text-orange-400">⚠️</span>'}
                            </p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button onclick="event.stopPropagation(); UI.openModal('edit-category-modal', {id: ${category.id}, name: '${category.name}'})" class="p-3 hover:bg-blue-900 hover:bg-opacity-30 rounded-lg transition-all duration-300 text-blue-400 transform hover:scale-110" title="Редактировать">✏️</button>
                        <button onclick="event.stopPropagation(); App.handleDeleteCategory(${category.id})" class="p-3 hover:bg-red-900 hover:bg-opacity-30 rounded-lg transition-all duration-300 text-red-400 transform hover:scale-110" title="Удалить категорию">🗑️</button>
                        <div class="text-gray-400 transition-transform duration-300 ${hasQuestions ? 'rotate-0' : 'rotate-90'}">
                            ${hasQuestions ? '👇' : '👉'}
                        </div>
                    </div>
                </div>
                ${questionsHtml}
            </div>`;
    },

    toggleQuestionsVisibility(categoryId) {
        const list = document.getElementById(`questions-${categoryId}`);
        if (list) {
            list.classList.toggle('expanded');

            // Анимация иконки
            const item = list.closest('.management-item');
            const icon = item.querySelector('.flex.items-center.space-x-2 > div:last-child');
            if (icon) {
                icon.classList.toggle('rotate-0');
                icon.classList.toggle('rotate-90');
            }
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

        // Анимация появления модального окна
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        modal.style.opacity = '0';
        modal.style.transform = 'scale(0.95)';

        setTimeout(() => {
            modal.style.opacity = '1';
            modal.style.transform = 'scale(1)';
        }, 10);
    },

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            // Анимация скрытия модального окна
            modal.style.opacity = '0';
            modal.style.transform = 'scale(0.95)';

            setTimeout(() => {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }, 200);
        }
    },

    renderAllModals() {
        this.elements.modalsContainer.innerHTML = `
            <!-- Answer Modal -->
            <div id="answer-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black bg-opacity-80 p-4 transition-all duration-300">
                <div class="relative w-full max-w-4xl max-h-[90vh] glass-light rounded-2xl shadow-2xl flex flex-col overflow-hidden transform transition-all duration-300">
                    <div class="flex items-start justify-between p-6 border-b border-gradient-to-r from-blue-500/30 to-purple-500/30">
                        <div class="flex items-center gap-3">
                            <span class="text-2xl animate-pulse">❓</span>
                            <div id="modal-question" class="text-xl font-semibold text-gray-200 leading-relaxed flex-1"></div>
                        </div>
                        <button type="button" class="modal-close-btn text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg p-2 transition-all duration-300 transform hover:scale-110">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                    <div class="flex items-center gap-2 px-6 py-2 bg-green-500/10 border-b border-green-500/20">
                        <span class="text-green-400">💡</span>
                        <span class="text-sm text-green-300">Ответ</span>
                    </div>
                    <div id="modal-answer" class="p-6 overflow-y-auto text-gray-300 leading-relaxed custom-scrollbar flex-1"></div>
                </div>
            </div>

            <!-- Edit Category Modal -->
            <div id="edit-category-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black bg-opacity-80 p-4 transition-all duration-300">
                 <div class="relative w-full max-w-md glass-light rounded-xl shadow-2xl transform transition-all duration-300">
                    <div class="flex items-center justify-between p-6 border-b border-blue-500 border-opacity-30">
                        <div class="flex items-center gap-3">
                            <span class="text-xl">📝</span>
                            <h3 class="text-xl font-semibold text-gray-200">Редактировать категорию</h3>
                        </div>
                        <button type="button" class="modal-close-btn text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg p-2 transition-all duration-300 transform hover:scale-110">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                    <form id="edit-category-form" class="p-6">
                        <input type="hidden" id="edit-category-id">
                        <div class="mb-6">
                            <label for="edit-category-name" class="block mb-2 text-sm font-medium text-gray-300 flex items-center gap-2">
                                <span>🏷️</span> Новое название
                            </label>
                            <input type="text" id="edit-category-name" required class="w-full form-input rounded-lg p-3 focus:ring-2 focus:ring-blue-500 transition-all">
                        </div>
                        <button type="submit" class="w-full btn-success font-medium rounded-lg px-5 py-3 transition-all transform hover:scale-105">
                            💾 Сохранить изменения
                        </button>
                    </form>
                </div>
            </div>

            <!-- Edit Question Modal -->
            <div id="edit-question-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black bg-opacity-80 p-4 transition-all duration-300">
                <div class="relative w-full max-w-2xl glass-light rounded-xl shadow-2xl transform transition-all duration-300">
                    <div class="flex items-center justify-between p-6 border-b border-blue-500 border-opacity-30">
                        <div class="flex items-center gap-3">
                            <span class="text-xl">📝</span>
                            <h3 class="text-xl font-semibold text-gray-200">Редактировать вопрос</h3>
                        </div>
                        <button type="button" class="modal-close-btn text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg p-2 transition-all duration-300 transform hover:scale-110">
                           <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                    <form id="edit-question-form" class="p-6 space-y-4">
                        <input type="hidden" id="edit-question-id">
                        <div>
                            <label for="edit-question-category" class="block mb-2 text-sm font-medium text-gray-300 flex items-center gap-2">
                                <span>📂</span> Категория
                            </label>
                            <select id="edit-question-category" required class="w-full form-input rounded-lg p-3 focus:ring-2 focus:ring-blue-500 transition-all"></select>
                        </div>
                        <div>
                            <label for="edit-question-text" class="block mb-2 text-sm font-medium text-gray-300 flex items-center gap-2">
                                <span>❓</span> Вопрос
                            </label>
                            <textarea id="edit-question-text" rows="3" required class="w-full form-input rounded-lg p-3 resize-none focus:ring-2 focus:ring-blue-500 transition-all"></textarea>
                        </div>
                        <div>
                            <label for="edit-answer-text" class="block mb-2 text-sm font-medium text-gray-300 flex items-center gap-2">
                                <span>💡</span> Ответ
                            </label>
                            <textarea id="edit-answer-text" rows="6" required class="w-full form-input rounded-lg p-3 resize-none focus:ring-2 focus:ring-blue-500 transition-all"></textarea>
                        </div>
                        <button type="submit" class="w-full btn-primary font-medium rounded-lg px-5 py-3 transition-all transform hover:scale-105">
                            💾 Сохранить изменения
                        </button>
                    </form>
                </div>
            </div>

            <!-- Confirmation Modal -->
            <div id="confirm-modal" class="fixed inset-0 z-[100] hidden items-center justify-center bg-black bg-opacity-80 p-4 transition-all duration-300">
                <div class="relative w-full max-w-md glass-light rounded-xl shadow-2xl transform transition-all duration-300">
                    <div class="p-6 text-center">
                        <div class="mx-auto mb-4 h-16 w-16 text-orange-500 text-6xl animate-bounce">⚠️</div>
                        <h3 class="mb-5 text-xl font-semibold text-gray-300">Подтверждение действия</h3>
                        <p id="confirm-modal-text" class="mb-6 text-lg text-gray-400"></p>
                        <div class="flex space-x-4">
                            <button id="confirm-modal-yes" class="flex-1 btn-danger font-medium rounded-lg px-5 py-3 transition-all transform hover:scale-105">
                                🗑️ Да, удалить
                            </button>
                            <button id="confirm-modal-no" class="flex-1 text-gray-300 hover:text-white hover:bg-gray-700 rounded-lg border border-gray-600 font-medium px-5 py-3 transition-all transform hover:scale-105">
                                ❌ Отменить
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
};

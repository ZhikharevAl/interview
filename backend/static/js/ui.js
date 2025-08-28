const UI = {
    // DOM element references
    elements: {
        categorySelect: null,
        questionCategorySelect: null,
        cardsContainer: null,
        loadingDiv: null,
        messageContainer: null,
        statsContainer: null,
        modal: null,
        modalQuestion: null,
        modalAnswer: null,
        modalCloseBtn: null
    },

    /**
     * Initialize DOM element references
     */
    initElements() {
        this.elements = {
            categorySelect: document.getElementById('category-select'),
            questionCategorySelect: document.getElementById('question-category'),
            cardsContainer: document.getElementById('cards-container'),
            loadingDiv: document.getElementById('loading'),
            messageContainer: document.getElementById('message-container'),
            statsContainer: document.getElementById('stats-container'),
            modal: document.getElementById('answer-modal'),
            modalQuestion: document.getElementById('modal-question'),
            modalAnswer: document.getElementById('modal-answer'),
            modalCloseBtn: document.getElementById('modal-close-btn')
        };
    },

    /**
     * Show/hide loading indicator
     * @param {boolean} show - Whether to show loading
     */
    toggleLoading(show) {
        this.elements.loadingDiv.style.display = show ? 'block' : 'none';
    },

    /**
     * Display message to user
     * @param {string} text - Message text
     * @param {string} type - Message type (success, error)
     */
    showMessage(text, type = 'success') {
        const styles = type === 'success'
            ? 'bg-green-100 border-green-400 text-green-800'
            : 'bg-red-100 border-red-400 text-red-800';

        this.elements.messageContainer.innerHTML = `
            <div class="border ${styles} px-4 py-3 rounded relative" role="alert">
                ${text}
            </div>
        `;

        setTimeout(() => {
            this.elements.messageContainer.innerHTML = '';
        }, CONFIG.UI.MESSAGE_TIMEOUT);
    },

    /**
     * Populate select element with options
     * @param {HTMLSelectElement} selectElement - Select element
     * @param {Array} options - Options array
     * @param {string} defaultText - Default option text
     */
    populateSelect(selectElement, options, defaultText = '') {
        selectElement.innerHTML = defaultText ? `<option value="">${defaultText}</option>` : '';
        options.forEach(option => {
            const optionElement = new Option(option.name, option.id);
            selectElement.add(optionElement);
        });
    },

    /**
     * Render statistics cards
     * @param {number} categoriesCount - Number of categories
     * @param {number} questionsCount - Number of questions
     */
    renderStats(categoriesCount, questionsCount) {
        this.elements.statsContainer.innerHTML = `
            <div class="stat-card bg-white/60 p-6 rounded-lg shadow-md border border-gray-200 text-center">
                <div class="stat-number text-4xl font-bold text-[#111111]">${categoriesCount}</div>
                <div class="stat-label text-sm font-medium text-gray-600 mt-1">Категорий</div>
            </div>
            <div class="stat-card bg-white/60 p-6 rounded-lg shadow-md border border-gray-200 text-center">
                <div class="stat-number text-4xl font-bold text-[#111111]">${questionsCount}</div>
                <div class="stat-label text-sm font-medium text-gray-600 mt-1">Всего вопросов</div>
            </div>
        `;
    },

    /**
     * Render error message in stats container
     * @param {string} message - Error message
     */
    renderStatsError(message = 'Не удалось загрузить статистику.') {
        this.elements.statsContainer.innerHTML = `<p class="text-red-600">${message}</p>`;
    },

    /**
     * Render question cards
     * @param {Array} questions - Questions array
     */
    renderQuestions(questions) {
        this.elements.cardsContainer.innerHTML = '';

        if (questions.length === 0) {
            this.elements.cardsContainer.innerHTML = `
                <p class="text-center text-gray-500 col-span-full py-10">
                    В этой категории пока нет вопросов. Добавьте их во вкладке "Управление"!
                </p>
            `;
            return;
        }

        questions.forEach((question, index) => {
            const card = this.createQuestionCard(question, index);
            this.elements.cardsContainer.appendChild(card);
        });
    },

    /**
     * Create individual question card element
     * @param {Object} question - Question data
     * @param {number} index - Card index for animation delay
     * @returns {HTMLElement} Card element
     */
    createQuestionCard(question, index) {
        const card = document.createElement('div');
        card.className = 'fade-in-card question-card text-[#111111] p-6 flex items-center justify-center rounded-xl shadow-lg cursor-pointer';
        card.style.minHeight = CONFIG.UI.CARD_MIN_HEIGHT;
        card.style.animationDelay = `${index * CONFIG.UI.ANIMATION_DELAY}ms`;

        const formattedQuestion = Utils.formatText(question.question_text);
        const formattedAnswer = Utils.formatText(question.answer_text);

        card.innerHTML = `<div class="text-center text-lg font-semibold">${formattedQuestion}</div>`;

        card.addEventListener('click', () => {
            this.openModal(formattedQuestion, formattedAnswer);
        });

        return card;
    },

    /**
     * Render error message in cards container
     * @param {string} message - Error message
     */
    renderCardsError(message = 'Не удалось загрузить вопросы. Проверьте подключение к серверу.') {
        this.elements.cardsContainer.innerHTML = `
            <p class="text-center text-red-600 col-span-full">${message}</p>
        `;
    },

    /**
     * Open modal with question and answer
     * @param {string} questionHTML - Formatted question HTML
     * @param {string} answerHTML - Formatted answer HTML
     */
    openModal(questionHTML, answerHTML) {
        this.elements.modalQuestion.innerHTML = questionHTML;
        this.elements.modalAnswer.innerHTML = answerHTML;
        this.elements.modal.classList.remove('hidden');
        this.elements.modal.classList.add('flex');
    },

    /**
     * Close modal
     */
    closeModal() {
        this.elements.modal.classList.add('hidden');
        this.elements.modal.classList.remove('flex');
        this.elements.modalQuestion.innerHTML = '';
        this.elements.modalAnswer.innerHTML = '';
    },

    /**
     * Switch between tabs
     * @param {string} tabName - Tab name to switch to
     * @param {Event} event - Click event
     */
    switchTab(tabName, event) {
        // Remove active class from all tab buttons
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });

        // Hide all tab panes
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.add('hidden');
        });

        // Activate clicked tab
        event.target.classList.add('active');
        document.getElementById(tabName + '-tab').classList.remove('hidden');
    },

    /**
     * Initialize event listeners
     */
    initEventListeners() {
        // Modal close events
        this.elements.modalCloseBtn.addEventListener('click', () => this.closeModal());
        this.elements.modal.addEventListener('click', (event) => {
            if (event.target === this.elements.modal) {
                this.closeModal();
            }
        });

        // Category select change
        this.elements.categorySelect.addEventListener('change', (event) => {
            App.loadQuestions(event.target.value);
        });
    }
};

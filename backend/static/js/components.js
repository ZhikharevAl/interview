const Components = {
    /**
     * Create loading spinner component
     * @returns {string} HTML string for loading spinner
     */
    loadingSpinner() {
        return `
            <div role="status">
                <svg aria-hidden="true" class="inline w-8 h-8 text-gray-300 animate-spin fill-[#74070c]"
                    viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                        fill="currentColor" />
                    <path
                        d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0492C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                        fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
            </div>
        `;
    },

    /**
     * Create shuffle button component
     * @returns {string} HTML string for shuffle button
     */
    shuffleButton() {
        return `
            <button onclick="shuffleCards()"
                class="w-full md:w-auto inline-flex items-center justify-center px-5 py-2.5 text-sm font-medium text-center bg-white border border-[#B0ADF2] text-[#111111] rounded-lg hover:bg-[#B0ADF2] hover:text-white focus:ring-4 focus:outline-none focus:ring-[#B0ADF2]/50 transition-colors">
                ${this.shuffleIcon()}
                Перемешать
            </button>
        `;
    },

    /**
     * Create shuffle icon
     * @returns {string} SVG icon HTML
     */
    shuffleIcon() {
        return `
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="mr-2">
                <polyline points="16 3 21 3 21 8"></polyline>
                <line x1="4" y1="20" x2="21" y2="3"></line>
                <polyline points="21 16 21 21 16 21"></polyline>
                <line x1="15" y1="15" x2="21" y2="21"></line>
                <line x1="4" y1="4" x2="9" y2="9"></line>
            </svg>
        `;
    },

    /**
     * Create close button for modal
     * @returns {string} HTML string for close button
     */
    closeButton() {
        return `
            <button type="button" id="modal-close-btn"
                class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clip-rule="evenodd"></path>
                </svg>
            </button>
        `;
    },

    /**
     * Create stat card component
     * @param {number} value - Stat value
     * @param {string} label - Stat label
     * @returns {string} HTML string for stat card
     */
    statCard(value, label) {
        return `
            <div class="stat-card bg-white/60 p-6 rounded-lg shadow-md border border-gray-200 text-center">
                <div class="stat-number text-4xl font-bold text-[#111111]">${value}</div>
                <div class="stat-label text-sm font-medium text-gray-600 mt-1">${label}</div>
            </div>
        `;
    },

    /**
     * Create alert/message component
     * @param {string} message - Message text
     * @param {string} type - Alert type (success, error, info, warning)
     * @returns {string} HTML string for alert
     */
    alert(message, type = 'info') {
        const styles = {
            success: 'bg-green-100 border-green-400 text-green-800',
            error: 'bg-red-100 border-red-400 text-red-800',
            warning: 'bg-yellow-100 border-yellow-400 text-yellow-800',
            info: 'bg-blue-100 border-blue-400 text-blue-800'
        };

        return `
            <div class="border ${styles[type]} px-4 py-3 rounded relative" role="alert">
                ${message}
            </div>
        `;
    },

    /**
     * Create empty state component
     * @param {string} message - Empty state message
     * @param {string} actionText - Action button text (optional)
     * @param {string} actionOnClick - Action button onclick (optional)
     * @returns {string} HTML string for empty state
     */
    emptyState(message, actionText = null, actionOnClick = null) {
        const actionButton = actionText && actionOnClick
            ? `<button onclick="${actionOnClick}" class="button-primary mt-4">${actionText}</button>`
            : '';

        return `
            <div class="text-center text-gray-500 col-span-full py-10">
                <p class="mb-4">${message}</p>
                ${actionButton}
            </div>
        `;
    },

    /**
     * Create form input group component
     * @param {Object} config - Input configuration
     * @returns {string} HTML string for input group
     */
    inputGroup({ id, label, type = 'text', placeholder = '', required = false, rows = null }) {
        const isTextarea = type === 'textarea';
        const requiredAttr = required ? 'required' : '';
        const rowsAttr = rows ? `rows="${rows}"` : '';

        const inputElement = isTextarea
            ? `<textarea id="${id}" ${requiredAttr} ${rowsAttr} placeholder="${placeholder}"
                class="block p-2.5 w-full text-sm text-[#111111] bg-white rounded-lg border border-gray-300 focus:ring-[#74070c] focus:border-[#74070c] placeholder-gray-500"></textarea>`
            : `<input type="${type}" id="${id}" ${requiredAttr} placeholder="${placeholder}"
                class="bg-white border border-gray-300 text-[#111111] text-sm rounded-lg focus:ring-[#74070c] focus:border-[#74070c] block w-full p-2.5 placeholder-gray-500">`;

        return `
            <div>
                <label for="${id}" class="block mb-2 text-sm font-medium text-gray-700">${label}</label>
                ${inputElement}
            </div>
        `;
    },

    /**
     * Create select input component
     * @param {Object} config - Select configuration
     * @returns {string} HTML string for select
     */
    selectGroup({ id, label, options = [], placeholder = '', required = false }) {
        const requiredAttr = required ? 'required' : '';
        const placeholderOption = placeholder ? `<option value="">${placeholder}</option>` : '';

        const optionElements = options.map(option =>
            `<option value="${option.value}">${option.text}</option>`
        ).join('');

        return `
            <div>
                <label for="${id}" class="block mb-2 text-sm font-medium text-gray-700">${label}</label>
                <select id="${id}" ${requiredAttr}
                    class="bg-white border border-gray-300 text-[#111111] text-sm rounded-lg focus:ring-[#74070c] focus:border-[#74070c] block w-full p-2.5 placeholder-gray-500">
                    ${placeholderOption}
                    ${optionElements}
                </select>
            </div>
        `;
    }
};

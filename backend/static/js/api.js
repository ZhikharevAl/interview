const API = {
    /**
     * Generic fetch wrapper
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Fetch options
     * @returns {Promise} API response
     */
    async request(endpoint, options = {}) {
        try {
            const response = await fetch(`${CONFIG.API_URL}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error for ${endpoint}:`, error);
            throw error;
        }
    },

    // Categories API
    categories: {
        /**
         * Get all categories
         * @param {number} skip - Number of items to skip
         * @param {number} limit - Number of items to fetch
         * @returns {Promise<Array>} Categories list
         */
        async getAll(skip = 0, limit = 100) {
            return API.request(`/categories/?skip=${skip}&limit=${limit}`);
        },

        /**
         * Create new category
         * @param {Object} categoryData - Category data
         * @returns {Promise<Object>} Created category
         */
        async create(categoryData) {
            return API.request('/categories/', {
                method: 'POST',
                body: JSON.stringify(categoryData)
            });
        }
    },

    // Questions API
    questions: {
        /**
         * Get all questions or by category
         * @param {number|null} categoryId - Category ID filter
         * @returns {Promise<Array>} Questions list
         */
        async getAll(categoryId = null) {
            const url = categoryId ? `/questions/?category_id=${categoryId}` : '/questions/';
            return API.request(url);
        },

        /**
         * Create new question
         * @param {Object} questionData - Question data
         * @returns {Promise<Object>} Created question
         */
        async create(questionData) {
            return API.request('/questions/', {
                method: 'POST',
                body: JSON.stringify(questionData)
            });
        }
    }
};

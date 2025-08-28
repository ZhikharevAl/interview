const Utils = {
    /**
     * Format text with markdown-like syntax
     * @param {string} text - Text to format
     * @returns {string} Formatted HTML
     */
    formatText(text) {
        const sanitizer = new DOMParser();
        let sanitizedText = sanitizer.parseFromString(text, 'text/html').body.textContent || "";

        // Format code blocks
        sanitizedText = sanitizedText.replace(/```([\s\S]*?)```/g, (match, code) => {
            const encodedCode = code.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            return `<pre class="bg-white text-[#111111] p-4 rounded-md text-sm overflow-x-auto my-4 border border-gray-200">${encodedCode.trim()}</pre>`;
        });

        // Format inline code
        sanitizedText = sanitizedText.replace(/`([^`]+)`/g, '<code class="bg-gray-200 text-[#111111] font-mono text-sm px-1.5 py-0.5 rounded-md">$1</code>');

        // Format bold text
        sanitizedText = sanitizedText.replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-inherit">$1</strong>');

        // Convert to paragraphs
        let result = '';
        const parts = sanitizedText.split(/(<pre[\s\S]*?<\/pre>)/);
        parts.forEach(part => {
            if (part.startsWith('<pre')) {
                result += part;
            } else {
                result += '<p>' + part.trim().replace(/\n\s*\n/g, '</p><p>').replace(/\n/g, '<br>') + '</p>';
            }
        });

        return result.replace(/<p><\/p>|(<p><br><\/p>)/g, '');
    },

    /**
     * Shuffle array elements
     * @param {Array} array - Array to shuffle
     * @returns {Array} Shuffled array
     */
    shuffleArray(array) {
        return [...array].sort(() => Math.random() - 0.5);
    },

    /**
     * Debounce function execution
     * @param {Function} func - Function to debounce
     * @param {number} delay - Delay in milliseconds
     * @returns {Function} Debounced function
     */
    debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    },

    /**
     * Validate form data
     * @param {Object} data - Form data to validate
     * @param {Array} requiredFields - Required field names
     * @returns {Object} Validation result
     */
    validateFormData(data, requiredFields) {
        const errors = [];

        requiredFields.forEach(field => {
            if (!data[field] || (typeof data[field] === 'string' && !data[field].trim())) {
                errors.push(`Field ${field} is required`);
            }
        });

        return {
            isValid: errors.length === 0,
            errors
        };
    }
};

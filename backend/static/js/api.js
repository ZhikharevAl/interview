const API = {
    async request(endpoint, options = {}) {
        try {
            const response = await fetch(`${CONFIG.API_URL}${endpoint}`, {
                headers: { 'Content-Type': 'application/json', ...options.headers },
                ...options
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
            }
            if (response.status === 204 || response.headers.get("content-length") === "0") {
                return null;
            }
            return await response.json();
        } catch (error) {
            console.error(`API Error for ${endpoint}:`, error);
            throw error;
        }
    },
    categories: {
        getAll: () => API.request(`/categories/`),
        create: (data) => API.request('/categories/', { method: 'POST', body: JSON.stringify(data) }),
        update: (id, data) => API.request(`/categories/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
        delete: (id) => API.request(`/categories/${id}`, { method: 'DELETE' })
    },
    questions: {
        getAll: (categoryId = null) => API.request(categoryId ? `/questions/?category_id=${categoryId}` : '/questions/'),
        create: (data) => API.request('/questions/', { method: 'POST', body: JSON.stringify(data) }),
        update: (id, data) => API.request(`/questions/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
        delete: (id) => API.request(`/questions/${id}`, { method: 'DELETE' })
    }
};

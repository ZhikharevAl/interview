const getApiBaseUrl = () => {
    if (window.location.hostname === 'localhost' && window.location.port === '8080') {
        return 'http://localhost:8080/api/v1';
    }
    return '/api/v1';
};

const API_BASE = getApiBaseUrl();

const CONFIG = {
    questionsPerPage: 12,
    notificationDuration: 3000,
    maxVisiblePages: 5,
    geometricShapesCount: 20
};

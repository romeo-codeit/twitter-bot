import axios from 'axios';

// Create an Axios instance with a base URL for the backend
const api = axios.create({
  baseURL: 'http://localhost:5001/api', // The port matches our Flask backend
  withCredentials: true, // This is important for session cookies to be sent
});

// --- Auth API Calls ---
export const registerUser = (username, password) => api.post('/auth/register', { username, password });
export const loginUser = (username, password) => api.post('/auth/login', { username, password });
export const logoutUser = () => api.post('/auth/logout');
export const getAuthStatus = () => api.get('/auth/status');

// --- Bot API Calls ---

// Twitter Connection
export const connectTwitterApi = (keys) => api.post('/bot/twitter/connect', keys);
export const getTwitterStatusApi = () => api.get('/bot/twitter/status');

// Content Queue
export const getContentApi = () => api.get('/bot/content');
export const addContentApi = (contentData) => api.post('/bot/content', contentData);
export const updateContentApi = (id, contentData) => api.put(`/bot/content/${id}`, contentData);
export const deleteContentApi = (id) => api.delete(`/bot/content/${id}`);

// Schedule
export const getScheduleApi = () => api.get('/bot/schedule');
export const setScheduleApi = (times) => api.post('/bot/schedule', { times });

// History
export const getHistoryApi = () => {
    // This endpoint doesn't exist yet, but we can add it here for completeness
    // return api.get('/bot/history');
    console.warn("getHistoryApi is a placeholder as the endpoint is not yet implemented.");
    return Promise.resolve({ data: [] }); // Return empty data for now
};

// --- Thread API Calls ---
export const createThreadApi = (threadData) => api.post('/bot/threads', threadData);
export const getThreadsApi = () => api.get('/bot/threads');
export const getThreadDetailsApi = (threadId) => api.get(`/bot/threads/${threadId}`);

// --- Auto-Reply API Calls ---
export const getAutoReplySettingsApi = () => api.get('/autoreply/settings');
export const setAutoReplySettingsApi = (settings) => api.post('/autoreply/settings', settings);
export const getAutoReplyTemplatesApi = () => api.get('/autoreply/templates');
export const addAutoReplyTemplateApi = (templateData) => api.post('/autoreply/templates', templateData);
export const deleteAutoReplyTemplateApi = (id) => api.delete(`/autoreply/templates/${id}`);


export default api;

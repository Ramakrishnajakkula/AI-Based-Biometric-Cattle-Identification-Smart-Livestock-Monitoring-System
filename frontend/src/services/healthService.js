/**
 * Health Service — Alerts and prediction APIs
 */
import api from './api';

export const healthService = {
  getAlerts: async (params = {}) => {
    const { data } = await api.get('/health/alerts', { params });
    return data;
  },

  resolveAlert: async (alertId) => {
    const { data } = await api.put(`/health/alerts/${alertId}/resolve`);
    return data;
  },

  predictByTagId: async (tagId) => {
    const { data } = await api.post('/health/predict', { tag_id: tagId });
    return data;
  },

  predictByFeatures: async (features) => {
    const { data } = await api.post('/health/predict', { features });
    return data;
  },
};

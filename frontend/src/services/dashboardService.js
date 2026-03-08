/**
 * Dashboard Service — Stats and recent data
 * Author: Poshith
 */
import api from './api';

export const dashboardService = {
  getStats: async () => {
    const { data } = await api.get('/dashboard/stats');
    return data;
  },

  getRecentAlerts: async () => {
    const { data } = await api.get('/dashboard/recent-alerts');
    return data;
  },
};

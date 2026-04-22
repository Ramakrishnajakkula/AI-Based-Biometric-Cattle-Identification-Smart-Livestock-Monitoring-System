/**
 * Admin Service — Admin dashboard and user management APIs
 */
import api from './api';

export const adminService = {
  getStats: async () => {
    const { data } = await api.get('/admin/stats');
    return data;
  },

  getUsers: async () => {
    const { data } = await api.get('/admin/users');
    return data;
  },

  updateUserRole: async (userId, role) => {
    const { data } = await api.put(`/admin/users/${userId}/role`, { role });
    return data;
  },

  getClaims: async (params = {}) => {
    const { data } = await api.get('/admin/claims', { params });
    return data;
  },
};

/**
 * Cattle Service — CRUD operations
 * Author: Poshith
 */
import api from './api';

export const cattleService = {
  list: async (params) => {
    const { data } = await api.get('/cattle', { params });
    return data;
  },

  getById: async (id) => {
    const { data } = await api.get(`/cattle/${id}`);
    return data;
  },

  register: async (cattleData) => {
    const { data } = await api.post('/cattle', cattleData);
    return data;
  },

  update: async (id, cattleData) => {
    const { data } = await api.put(`/cattle/${id}`, cattleData);
    return data;
  },

  delete: async (id) => {
    const { data } = await api.delete(`/cattle/${id}`);
    return data;
  },
};

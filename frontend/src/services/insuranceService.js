/**
 * Insurance Service — API calls for insurance claims
 * Author: Poshith
 */
import api from './api';

export const insuranceService = {
  list: async () => {
    const { data } = await api.get('/insurance/claims');
    return data;
  },

  create: async (payload) => {
    const { data } = await api.post('/insurance/claims', payload);
    return data;
  },

  getById: async (claimId) => {
    const { data } = await api.get(`/insurance/claims/${claimId}`);
    return data;
  },

  verify: async (claimId) => {
    const { data } = await api.post(`/insurance/claims/${claimId}/verify`);
    return data;
  },
};

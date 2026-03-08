/**
 * Sensor Service — Fetch sensor readings
 * Author: Poshith
 */
import api from './api';

export const sensorService = {
  getLatest: async (cattleId) => {
    const { data } = await api.get(`/sensors/${cattleId}/latest`);
    return data;
  },

  getHistory: async (cattleId, sensorType = 'temperature', hours = 24) => {
    const { data } = await api.get(`/sensors/${cattleId}/history`, {
      params: { type: sensorType, hours },
    });
    return data;
  },

  getGpsPositions: async () => {
    const { data } = await api.get('/sensors/gps');
    return data;
  },
};

/**
 * Socket.IO Service — Real-time WebSocket connection
 * Author: Poshith
 */
import { io } from 'socket.io-client';

let socket = null;

export const socketService = {
  connect: () => {
    if (!socket) {
      socket = io('/', { transports: ['websocket', 'polling'] });
      socket.on('connect', () => console.log('Socket connected'));
      socket.on('disconnect', () => console.log('Socket disconnected'));
    }
    return socket;
  },

  onSensorUpdate: (callback) => {
    const s = socketService.connect();
    s.on('sensor_update', callback);
  },

  onHealthAlert: (callback) => {
    const s = socketService.connect();
    s.on('health_alert', callback);
  },

  onGeofenceBreach: (callback) => {
    const s = socketService.connect();
    s.on('geofence_breach', callback);
  },

  disconnect: () => {
    if (socket) {
      socket.disconnect();
      socket = null;
    }
  },
};

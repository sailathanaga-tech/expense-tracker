/**
 * API Service Module
 * 
 * This module configures Axios for making HTTP requests to the backend.
 * 
 * Why this file exists:
 * - Centralizes API configuration
 * - Sets up base URL and default headers
 * - Provides a consistent way to make API calls
 */

import axios from 'axios'

// Create Axios instance with base configuration
const api = axios.create({
  baseURL: '/api',  // Uses Vite proxy to forward to backend
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add request interceptor to include JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api

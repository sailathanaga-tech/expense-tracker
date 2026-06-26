/**
 * React Application Entry Point
 * 
 * This file initializes the React application and renders it to the DOM.
 * 
 * Why this file exists:
 * - Entry point for the React application
 * - Mounts the App component to the DOM
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

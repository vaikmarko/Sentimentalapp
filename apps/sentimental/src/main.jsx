import React from 'react'
import { createRoot } from 'react-dom/client'
import SentimentalApp from './sentimental-app.jsx'
import './index.css'

createRoot(document.getElementById('sentimental-app')).render(<SentimentalApp />)

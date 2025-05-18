// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBR6GetAyWiU-uJURAqMhPUoV_gtF3ZNaE",
  authDomain: "sentimental-28cc9.firebaseapp.com",
  projectId: "sentimental-28cc9",
  storageBucket: "sentimental-28cc9.firebasestorage.app",
  messagingSenderId: "1025198101203",
  appId: "1:1025198101203:web:7327908c5e9dc148197a26"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Get a reference to services
const db = firebase.firestore();
const storage = firebase.storage();

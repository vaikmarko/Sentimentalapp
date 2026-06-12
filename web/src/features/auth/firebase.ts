import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Public web config (not a secret). Override per environment via Vite env vars.
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY ?? "AIzaSyCSoWmKZRDpXF5MlgWKEV6kWHc5xFMMm_I",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN ?? "sentimental-f95e6.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID ?? "sentimental-f95e6",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET ?? "sentimental-f95e6.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID ?? "319737737925",
  appId: import.meta.env.VITE_FIREBASE_APP_ID ?? "1:319737737925:web:1de7aa284a63ad9f9eb6ac",
};

export const firebaseApp = initializeApp(firebaseConfig);
export const auth = getAuth(firebaseApp);

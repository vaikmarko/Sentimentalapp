#!/bin/bash
set -e

echo "🏗️  Building Sentimental Apps..."

# Build Sentimental (direct JSX loading, no bundler yet)
echo "Building Sentimental app..."
mkdir -p public/js
cp apps/sentimental/sentimental-app.jsx public/js/sentimental-app.jsx
cp public/js/sentimental-app.jsx static/js/sentimental-app.jsx

# Copy shared assets
echo "Copying shared assets..."
mkdir -p public/css public/icons
cp shared/styles/css/*.css public/css/
cp shared/assets/icons/* public/icons/ 2>/dev/null || true
cp shared/config/firebase.json .
cp shared/config/firestore.rules .

echo "✅ Build complete!"

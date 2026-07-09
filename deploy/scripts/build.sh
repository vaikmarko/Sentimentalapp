#!/bin/bash
set -e

echo "🏗️  Building Sentimental Apps..."

# Build Sentimental frontend with Vite (outputs to public/)
echo "Building Sentimental app (Vite)..."
rm -rf public/assets
(cd apps/sentimental && npm run build)

# Flask serves the same built shell at / and /app
cp public/index.html templates/index.html

# Copy shared assets
echo "Copying shared assets..."
mkdir -p public/css public/icons
cp shared/styles/css/*.css public/css/
cp shared/assets/icons/* public/icons/ 2>/dev/null || true
cp shared/config/firebase.json .
cp shared/config/firestore.rules .

echo "✅ Build complete!"

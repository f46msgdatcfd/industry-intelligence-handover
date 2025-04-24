#!/bin/bash

echo "📦 Installing Python dependencies from requirements.txt ..."
echo ""

cd "$(dirname "$0")" || exit 1

if [ ! -f requirements.txt ]; then
    echo "❌ requirements.txt not found. Please ensure you're in the project root."
    exit 1
fi

pip install -r requirements.txt

echo ""
echo "✅ Environment setup complete."
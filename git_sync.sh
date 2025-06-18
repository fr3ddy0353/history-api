#!/bin/bash

echo "🔄 Pulling and rebasing from origin/main..."
git pull --rebase origin main

if [ $? -ne 0 ]; then
  echo "⚠️ Rebase failed! Resolve conflicts and run this script again."
  exit 1
fi

echo "✅ Rebase successful. Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
  echo "🎉 Push complete!"
else
  echo "❌ Push failed. Please check your network or GitHub permissions."
fi
#!/usr/bin/env bash
set -euo pipefail

if ! command -v flutter >/dev/null 2>&1; then
  echo 'Flutter SDK 3.22+ is required.' >&2
  exit 1
fi

flutter create \
  --empty \
  --platforms=android,ios \
  --org=com.daliilaykhidma \
  --project-name=dalil_app \
  .

python3 tool/configure_deep_links.py

flutter pub get
flutter gen-l10n
flutter analyze
flutter test

echo 'Native Android and iOS projects generated.'
echo 'Continue with FIREBASE_SETUP.md before enabling push notifications.'

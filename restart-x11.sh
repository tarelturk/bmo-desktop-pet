#!/usr/bin/env bash
set -euo pipefail
if [ "$(id -u)" = 0 ]; then
  echo 'Bu başlatıcıyı sudo olmadan çalıştırın.'
  exit 1
fi
pkill -TERM -x ChatGPT || true
for attempt in {1..30}; do
  if ! pgrep -x ChatGPT >/dev/null; then break; fi
  sleep 1
done
if pgrep -x ChatGPT >/dev/null; then
  echo 'ChatGPT henüz kapanmadı; zorla kapatılmadı. Menüden çıkıp tekrar deneyin.'
  exit 1
fi
exec chatgpt --ozone-platform=x11

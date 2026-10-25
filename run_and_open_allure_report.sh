#!/usr/bin/env bash
# Chạy test (lọc theo ID trong @allure.title nếu có), generate và mở Allure report.
# VD: bash run_and_open_allure_report.sh "GD02.1-02, GD03.1-01"
set -u

KEYWORDS="${1:-}"
if [ -z "$KEYWORDS" ]; then
  read -r -p "Nhập keyword (VD: GD02.1-02, GD03.1-01), Enter để chạy tất cả: " KEYWORDS
fi

if [ -d venv/Scripts ]; then PYTHON=venv/Scripts/python; elif [ -d venv/bin ]; then PYTHON=venv/bin/python; else PYTHON=python; fi

rm -rf allure-results allure-report

if [ -z "$KEYWORDS" ]; then
  "$PYTHON" -m pytest
else
  # Tìm tên hàm có @allure.title khớp ID, ghép thành biểu thức -k "a or b"
  EXPRESSION=$("$PYTHON" - "$KEYWORDS" <<'EOF'
import re
import sys
from pathlib import Path

keywords = [k.strip() for k in sys.argv[1].split(",") if k.strip()]
pattern = re.compile(r'@allure\.title\("([^"]+)"\)(?:.|\n)*?def (test_\w+)')
funcs = [
    func
    for path in sorted(Path("tests").glob("test_*.py"))
    for title, func in pattern.findall(path.read_text(encoding="utf-8"))
    if any(title.startswith(f"{k}:") for k in keywords)
]
print(" or ".join(funcs), end="")
EOF
)
  EXPRESSION="${EXPRESSION//$'\r'/}"
  if [ -z "$EXPRESSION" ]; then
    echo "Không tìm thấy test nào khớp: $KEYWORDS"
    exit 1
  fi
  "$PYTHON" -m pytest -k "$EXPRESSION"
fi

allure generate allure-results --clean -o allure-report && allure open allure-report

import os
import fitz  # PyMuPDF
import json
import re
from datetime import datetime

# PDF 폴더 경로
pdf_dir = os.path.join("scripts", "pdf")
digest_dir = os.path.join("public", "digests")
os.makedirs(digest_dir, exist_ok=True)

# 최신 PDF 파일 선택
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
if not pdf_files:
    print("❌ PDF 파일이 없습니다.")
    exit()

latest_pdf = max(pdf_files, key=lambda f: os.path.getmtime(os.path.join(pdf_dir, f)))
pdf_path = os.path.join(pdf_dir, latest_pdf)

# 날짜 추출 (파일명에서 250717 같은 부분 찾기)
match = re.search(r"(\d{6})", latest_pdf)
if not match:
    print("❌ 파일명에서 날짜를 추출할 수 없습니다.")
    exit()

raw_date = match.group(1)
date_obj = datetime.strptime("20" + raw_date, "%Y%m%d")
formatted_date = date_obj.strftime("%Y-%m-%d")

# 텍스트 추출
doc = fitz.open(pdf_path)
all_text = ""
for page in doc:
    all_text += page.get_text()
doc.close()

# index.json 업데이트
digest_entry = {
    "date": formatted_date,
    "file": f"{formatted_date}.html",
    "text": all_text[:300] + "..."  # 첫 300자만 저장 (예시)
}

index_file = os.path.join(digest_dir, "index.json")
try:
    with open(index_file, "r", encoding="utf-8") as f:
        index_data = json.load(f)
except:
    index_data = []

# 같은 날짜 있으면 제거 후 추가
index_data = [d for d in index_data if d["date"] != formatted_date]
index_data.insert(0, digest_entry)

with open(index_file, "w", encoding="utf-8") as f:
    json.dump(index_data, f, ensure_ascii=False, indent=2)

# 해당 날짜의 요약 HTML도 생성 (간단하게)
html_file = os.path.join(digest_dir, f"{formatted_date}.html")
with open(html_file, "w", encoding="utf-8") as f:
    f.write(f"<h1>{formatted_date} 요약</h1>\n<pre>{all_text[:2000]}</pre>")

print(f"✅ 요약 저장 완료: {formatted_date}")

import os
import subprocess
import re
from datetime import datetime

# Git 저장소 경로
repo_path = r"C:\Users\cwj\Desktop\stock-digest-site"
pdf_folder = os.path.join(repo_path, "scripts", "pdf")

# 최신 PDF 파일 찾기
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
if not pdf_files:
    print("❌ PDF 파일이 없습니다.")
    exit()

latest_pdf = max(pdf_files, key=lambda f: os.path.getmtime(os.path.join(pdf_folder, f)))
print(f"✅ 최신 PDF 파일: {latest_pdf}")

# 파일명에서 날짜 추출 (예: 250717 → 2025-07-17)
match = re.search(r'(\d{6})', latest_pdf)
if not match:
    print("❌ 파일명에서 날짜를 찾을 수 없습니다.")
    exit()

raw_date = match.group(1)  # 예: '250717'
date_obj = datetime.strptime("20" + raw_date, "%Y%m%d")
formatted_date = date_obj.strftime("%Y-%m-%d")

# Git으로 이동
os.chdir(repo_path)

# Git add, commit, push
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", f"자동 업로드: {formatted_date} PDF 반영"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print("🚀 GitHub에 커밋 및 푸시 완료")

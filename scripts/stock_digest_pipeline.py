# scripts/stock_digest_pipeline.py

import os
print("✅ Stock digest pipeline 실행 시작됨")

# 예시로 public/digests/index.json을 덮어씁니다
with open("public/digests/index.json", "w", encoding="utf-8") as f:
    f.write('{"status": "Success", "message": "Digest created."}')

print("✅ Digest 파일 생성 완료")

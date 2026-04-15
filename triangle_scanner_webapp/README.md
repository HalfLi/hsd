# KRX Triangle Scanner

한국 주식(KOSPI / KOSDAQ)에서 **삼각수렴 후보 종목**을 찾는 프로젝트입니다.

이 폴더에는 두 가지가 들어 있습니다.

1. **로컬 Streamlit 웹앱**
   - 브라우저에서 직접 조건을 조절하며 스캔
2. **데일리 자동 리포트 생성기**
   - GitHub Actions 또는 cron으로 매일 후보를 자동 생성

## 구성

- `app.py`  
  로컬에서 실행하는 Streamlit 앱
- `triangle_scanner_krx.py`  
  패턴 스캐너 엔진
- `scripts/daily_triangle_report.py`  
  CSV / JSON / Markdown 데일리 리포트 생성 스크립트
- `reports/`  
  자동 생성 결과 저장 폴더
- `../.github/workflows/triangle_scanner_daily.yml`  
  평일 자동 실행 워크플로

## 로컬 실행 (웹앱)

```bash
pip install -r triangle_scanner_webapp/requirements.txt
streamlit run triangle_scanner_webapp/app.py
```

## 로컬 실행 (데일리 리포트)

```bash
pip install -r triangle_scanner_webapp/requirements.txt
pip install tabulate
python triangle_scanner_webapp/scripts/daily_triangle_report.py \
  --market ALL \
  --top-n 30 \
  --max-tickers 900 \
  --output-dir triangle_scanner_webapp/reports
```

생성 파일 예시:

- `triangle_scanner_webapp/reports/latest_candidates.csv`
- `triangle_scanner_webapp/reports/latest_candidates.json`
- `triangle_scanner_webapp/reports/latest_report.md`
- `triangle_scanner_webapp/reports/latest_metadata.json`

## GitHub Actions 자동 갱신

`.github/workflows/triangle_scanner_daily.yml` 이 평일 18:10(KST)에 자동 실행됩니다.
원하면 GitHub Actions에서 수동 실행(`workflow_dispatch`)도 가능합니다.

자동 실행 시 리포트 파일이 저장소에 커밋됩니다.

## 중요한 점

이 프로젝트는 **자동매매가 아니라 후보 발굴기**입니다.  
차트 수동 검토 없이 바로 매수 판단하면 안 됩니다.

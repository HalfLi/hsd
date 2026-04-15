# KRX Triangle Scanner

한국 주식(KOSPI / KOSDAQ)에서 **삼각수렴 후보 종목**을 찾는 프로젝트입니다.

이 폴더에는 두 가지가 들어 있습니다.

1. **로컬 Streamlit 웹앱**
   - 브라우저에서 직접 조건을 조절하며 스캔
2. **GitHub Pages용 정적 대시보드 + GitHub Actions**
   - 장 마감 후 자동으로 결과를 갱신하고, GitHub Pages에서 결과만 바로 확인

## 구성

- `app.py`  
  로컬에서 실행하는 Streamlit 앱
- `triangle_scanner_krx.py`  
  패턴 스캐너 엔진
- `scripts/export_triangle_results.py`  
  정적 페이지에 뿌릴 JSON/CSV/차트 생성 스크립트
- `../docs/triangle-scanner/`  
  GitHub Pages에서 보게 될 정적 페이지
- `../.github/workflows/triangle_scanner_daily.yml`  
  매일 자동 스캔 워크플로

## 로컬 실행

```bash
pip install -r triangle_scanner_webapp/requirements.txt
streamlit run triangle_scanner_webapp/app.py
```

## GitHub Pages로 보기

이 리포에는 `docs/triangle-scanner/` 정적 페이지와 자동 갱신 워크플로가 포함되어 있습니다.

딱 한 번만 GitHub에서 아래를 켜면 됩니다.

1. **Settings**
2. **Pages**
3. **Build and deployment**
4. Source: **Deploy from a branch**
5. Branch: **main**
6. Folder: **/docs**

그 다음 주소는 보통 이렇게 됩니다.

- `https://halfli.github.io/hsd/triangle-scanner/`

## 자동 갱신

`.github/workflows/triangle_scanner_daily.yml` 이 평일 장 마감 후 결과를 다시 생성합니다.
원하면 GitHub Actions 화면에서 수동 실행도 가능합니다.

## 중요한 점

이 프로젝트는 **자동매매가 아니라 후보 발굴기**입니다.  
차트 수동 검토 없이 바로 매수 판단하면 안 됩니다.

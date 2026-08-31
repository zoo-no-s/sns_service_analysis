# sns_service_analysis

# 폴더 구조 설명
* ⚠️ 폴더 구조를 살펴보면 `*_dbt` 폴더 내에 필요 데이터 적재 및 분석 등을 통합적으로 관리할 수 있는 것으로 보입니다.
* 다만, 해당 프로젝트에서 기존 프로젝트 환경과 최대한 동일하게 구성해보았습니다.
* 아래에는 분석 진행 시 주요하게 접근하실 폴더에 대한 명세만 진행하도록 하겠습니다.
---
* 📂  `data` : 실제 분석 진행을 위한 데이터<br>
데이터 유출 및 용량 등의 문제로 인해서 깃 공유에서 제외하였습니다.<br>
데이터 공유는 csv 추출 후 각자 제공 예정입니다. (혹은 감당 가능한 요금이라면 빅쿼리에 직접 접근 하는 방식도 고려해보겠습니다)
  * `raw` : 전처리 전 원본 파일
  * `processed` : 전처리 완료 후 파일 (전처리 완료 파일, 분석용 마트 등...)

* 📂  `notebooks` : 분석 진행을 위한 노트북 파일 모음

* 📂  `src` : 전처리 수행용 파일

* 📋 `README.md` : (⚠️ 추후 프로젝트 설명으로 변경 필요 ⚠️)
  * 우선은 프로젝트 구조 설명 등과 같은 내용 작성 

* 📋 `requirements.txt` : 가상환경 패키지 목록
  * 저장 : `pip freeze > requirements.txt`
  * 설치 : `pip install -r requirements.txt`

---

# ⚙️ 프로젝트 진행을 위한 간단 깃(Git) 설명서

## 1. [환경 구축 시 단 한 번 수행]

### 1) 프로젝트 복사 (Clone)
```bash
git clone https://github.com/zoo-no-s/sns_service_analysis.git
cd sns_service_analysis
```

### 2) 가상환경 세팅 및 패키지 설치
```bash
# 가상환경 생성 (.venv)
python -m venv .venv

# 가상환경 활성화 (macOS / Linux)
source .venv/bin/activate

# 가상환경 활성화 (Windows PowerShell)
.venv\Scripts\Activate.ps1

# 가상환경 활성화 (Windows CMD)
.venv\Scripts\activate.bat

# 필수 패키지 일괄 설치
pip install -r requirements.txt
```

---

## 2. [기능 개발 시작 전 (매일 아침 / 새 작업 시작 시)]

*항상 `main` 브랜치의 최신 코드를 받아온 뒤, 작업용 브랜치를 새로 생성하여 시작합니다.*

```bash
# 1. main 브랜치로 이동
git switch main

# 2. 원격 저장소 최신 커밋 받아오기
git pull origin main

# 3. 새로운 작업 브랜치 생성 및 이동
git switch -c <새_브랜치명>
# 예: git switch -c feat/data-preprocessing
```

---

## 3. [작업 완료 후 반영 (개발 루틴)]

```bash
# 1. 변경된 파일 상태 확인
git status

# 2. 스테이징 영역에 변경사항 추가
git add .
# 또는 특정 파일만 추가: git add <파일명>

# 3. 커밋 메시지 작성
git commit -m "feat: 유저 활동 데이터 전처리 함수 구현"

# 4. 원격 저장소로 내 브랜치 업로드 (Push)
git push origin <내_브랜치명>
```

### 5) GitHub에서 PR(Pull Request) 생성
1. GitHub 저장소(`sns_service_analysis`) 페이지 접속
2. 상단에 뜨는 **`Compare & pull request`** 버튼 클릭
3. PR 제목 및 작업 내용 요약 작성
4. 우측 `Reviewers`에 리뷰할 팀원 지정 후 **Create pull request** 클릭

---

## 4. [필요에 따라 수행 (자주 쓰는 명령어)]

### 브랜치 전환 및 관리
```bash
# 현재 로컬 브랜치 목록 확인 (* 표시가 현재 위치)
git branch

# 원격 포함 모든 브랜치 확인
git branch -a

# 다른 기존 브랜치로 전환
git switch <이동할_브랜치명>

# 작업 완료되어 merge된 로컬 브랜치 삭제
git branch -d <삭제할_브랜치명>
```

### 작업 내용 임시 보관 (Stash)
*다른 브랜치로 급하게 넘어가야 하는데 작업 내용을 아직 커밋하기 애매할 때 사용합니다.*
```bash
# 현재 작업 내용 임시 저장
git stash

# 임시 저장된 작업 내용 다시 불러와 적용
git stash pop
```

### 가상환경 패키지 동기화
*새로운 라이브러리를 설치했다면 팀원들이 설치할 수 있도록 목록을 갱신합니다.*
```bash
pip freeze > requirements.txt
```

---

## 5. [브랜치 & 커밋 컨벤션]

### 브랜치 네이밍 규칙
* `feat/<기능명>`: 데이터 분석, 전처리, 신규 로직 구현 (예: `feat/user-retention-analysis`)
* `fix/<수정내용>`: 코드 에러 및 결측치 처리 로직 수정 (예: `fix/null-imputation-error`)
* `docs/<문서명>`: README, 보고서 등 문서 작성/수정 (예: `docs/git-guide`)
* `refactor/<내용>`: 결과 변경 없는 코드 구조 개선 및 모듈화 (예: `refactor/dataloader`)

### 커밋 메시지 접두사
* `feat:` 새로운 분석 로직/기능 구현
* `fix:` 버그 수정
* `docs:` 문서 수정 (README, 주석 등)
* `refactor:` 기능 변경 없는 코드 리팩토링
* `style:` 코드 포맷팅, 들여쓰기 수정 등 (코드 로직 영향 없음)

---

## ⚠️ [팀 협업 주의사항]
1. **`main` 브랜치에 직접 Push 금지:** 모든 작업은 개별 작업 브랜치에서 진행하며, 반드시 PR을 통해 코드 리뷰 후 병합합니다.
2. **코드 충돌(Conflict) 발생 시:** 임의로 강제 push/덮어쓰기를 하지 말고, 충돌 발생 시 팀원과 상의 후 해결합니다.
3. **대용량 파일 커밋 금지:** 원본 데이터셋(대용량 CSV/Parquet 등), 가상환경 폴더(`.venv`), 환경변수/인증키(`.env`)는 커밋하지 않도록 `.gitignore` 설정을 유지합니다.
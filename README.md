# Educinema

## 프로젝트 소개

**Educinema**는 영화와 교육을 결합한 플랫폼으로, 사용자가 영화와 관련된 기술 및 전공 정보를 공유하고 학습 자료를 제공할 수 있도록 설계되었습니다.  
이 프로젝트는 다음과 같은 문제를 해결하는 데 초점을 맞춥니다:
- 영화 속 기술과 전공 정보를 체계적으로 공유할 수 있는 공간 부족.
- 영화와 관련된 학습 자료를 쉽게 접근할 수 있는 플랫폼 부재.

### 주요 기능
- 사용자 인증 (회원가입, 로그인, 프로필 관리)
- 영화 관련 게시글 작성 및 관리
- 댓글 및 좋아요 기능
- 추천 게시글 제공
- 사용자 프로필 조회 및 활동 기록 확인

---

## 기술 스택

### Backend
- **Django Rest Framework (DRF)**: API 개발과 데이터 관리를 위한 백엔드 프레임워크.
- **JWT 인증**: 사용자 인증 및 보안 처리.

### Frontend
- **Vue.js**: 사용자 인터페이스 개발.
- **Pinia**: 상태 관리 라이브러리.
- **Vue Router**: 페이지 라우팅.

### 기타
- **Axios**: API 통신.
- **SQLite**: 데이터베이스 (개발 환경 기준).

---

## 설치 및 실행 방법

1. **저장소 클론**
   ```bash
   git clone https://github.com/your-repository/educinema.git
   cd educinema
   ```

2. **백엔드 설정**
   - 가상 환경 생성 및 활성화:
     ```bash
     python -m venv venv
     source venv\Scripts\activate
     ```
   - 의존성 설치:
     ```bash
     cd django-pjt
     pip install -r requirements.txt
     ```
   - 데이터베이스 마이그레이션:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
   - 서버 실행:
     ```bash
     python manage.py runserver
     ```

3. **프론트엔드 설정**
   - 의존성 설치:
     ```bash
     cd vue-project
     npm install
     ```
   - 개발 서버 실행:
     ```bash
     npm run dev
     ```

4. 웹 브라우저에서 [http://localhost:8000](http://localhost:8000), [http://localhost:5173/](http://localhost:5173/)로 접속하여 프로젝트 실행 확인.

---
## 프로젝트 구조

### Backend (django-pjt)
```bash
django-pjt/
├── accounts/          # 사용자 인증 및 프로필 관리
├── articles/          # 게시글 관리
├── comments/          # 댓글 기능
├── educinema/         # 프로젝트 설정
├── likes/            # 좋아요 기능
├── media/            # 미디어 파일 저장
│   └── movie_posters/  # 영화 포스터 이미지
├── movies/           # 영화 정보 관리
└── requirements.txt  # 의존성 목록
```

### Frontend (vue-project)
```bash
vue-project/
├── src/
│   ├── assets/       # 정적 파일
│   ├── components/   # Vue 컴포넌트
│   │   ├── ArticleList.vue
│   │   ├── ArticleListItem.vue
│   │   ├── UserProfileDetail.vue
│   │   └── UserProfileList.vue
│   ├── router/       # 라우팅 설정
│   │   └── index.js
│   └── stores/       # Pinia 상태 관리
│       ├── counter.js
│       ├── profileComments.js
│       └── user.js
└── package.json
```

## 주요 기능 상세

### 1. 게시글 관리
- 게시글 CRUD 기능
- 게시글 상세 정보:
  - 제목 및 내용
  - 영화 정보 (포스터, 제목)
  - 작성자 정보 (전공, 기술)
  - 작성/수정 일자
  - 좋아요 수
  - 댓글 수

### 2. 좋아요 시스템
- 게시글별 좋아요 토글 기능
- 실시간 좋아요 수 업데이트
- 사용자별 좋아요 목록 관리

### 3. 파일 관리
- 영화 포스터 이미지 저장 및 관리
- 학습 자료 파일 업로드/다운로드

### 4. 사용자 프로필
- 상세 프로필 정보 관리
- 작성 게시글 목록
- 활동 이력 (좋아요, 댓글)

## 데이터베이스 구조

### 주요 모델
- User: 사용자 정보
- Article: 게시글
- Comment: 댓글
- Like: 좋아요
- Movie: 영화 정보

## 보안 및 인증
- Token 기반 인증 시스템
- API 엔드포인트 권한 관리
- 민감한 사용자 정보 보호
---

## API 문서

API 문서는 Postman 또는 Swagger를 통해 제공됩니다. 주요 엔드포인트는 다음과 같습니다:

| Method | Endpoint                          | 설명                         |
|--------|-----------------------------------|------------------------------|
| POST   | `/api/users/`                     | 회원가입                    |
| POST   | `/api/users/login/`               | 로그인                      |
| GET    | `/api/posts/`                     | 게시글 목록 조회            |
| POST   | `/api/posts/`                     | 게시글 작성                 |
| GET    | `/api/posts/:id/`                 | 특정 게시글 상세 조회       |
| POST   | `/api/comments/`                  | 댓글 작성                   |
| POST   | `/api/likes/`                     | 좋아요 추가                 |

---

## 기여 방법

Educinema 프로젝트에 기여하고 싶다면 아래 단계를 따라주세요:

1. 저장소를 포크합니다.
2. 새로운 브랜치를 생성합니다 (`git checkout -b feature/new-feature`).
3. 변경 사항을 커밋합니다 (`git commit -m "Add new feature"`).
4. 브랜치에 푸시합니다 (`git push origin feature/new-feature`).
5. 풀 리퀘스트를 생성합니다.
***
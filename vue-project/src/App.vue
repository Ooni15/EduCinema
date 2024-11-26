<template>
  <header class="navbar">
    <!-- EduCinema -->
    <div class="navbar-left">
      <h1 class="navbar-title">EduCinema</h1>
    </div>
    <!-- 회원가입/로그인 버튼 -->
    <div class="navbar-right">
      <!-- 회원가입 페이지에서는 항상 로그인 버튼 표시 -->
      <div v-if="$route.name === 'SignUpView'">
        <RouterLink :to="{ name: 'LogInView' }" class="auth-button">로그인</RouterLink>
      </div>
      <!-- 로그인 상태에 따른 버튼 표시 -->
      <div v-else-if="store.isLogin">
        <form @submit.prevent="logOut" class="auth-button">
          <input type="submit" value="로그아웃" />
        </form>
      </div>
      <div v-else>
        <RouterLink :to="{ name: 'SignUpView' }" class="auth-button">회원가입</RouterLink>
      </div>
    </div>
    <!-- 게시글 메뉴 -->
    <nav class="navbar-menu">
      <RouterLink :to="{ name: 'ArticleView' }">게시글</RouterLink>
      <RouterLink :to="{ name: 'CreateView' }">게시글 작성</RouterLink>
      <RouterLink :to="{ name: 'ProfileListView' }">프로필</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();

const logOut = () => {
  store.logOut();
};
</script>

<style scoped>
/* Navbar 전체 레이아웃 */
.navbar {
  background-color: #f9f9f9; /* 전체 배경색 통일 */
  padding: 10px 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  position: relative; /* 상대적 기준 */
  box-shadow: none; /* 그림자 제거 */
}

/* EduCinema 제목 */
.navbar-left {
  display: flex;
  align-items: center;
  justify-content: flex-start; /* 왼쪽 정렬 */
  position: relative; /* 상대적 위치 */
}

.navbar-title {
  font-family: 'Pretendard', sans-serif;
  font-size: 32px;
  font-weight: bold;
  color: #333; /* 검정색 */
  margin: 0;
}

/* 회원가입/로그아웃 버튼 */
.navbar-right {
  position: absolute; /* 오른쪽 끝으로 고정 */
  top: 10px; /* EduCinema와 같은 높이 */
  right: 20px;
}

.auth-button {
  font-size: 16px;
  color: #888; /* 회색 */
  text-decoration: none;
  border: none;
  background: none;
  cursor: pointer;
}

.auth-button:hover {
  color: #0066FF; /* 마우스 오버 시 파란색 */
}

.auth-button input[type='submit'] {
  font-size: 16px;
  color: #888; /* 회색 */
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
}

.auth-button input[type='submit']:hover {
  color: #0066FF; /* 마우스 오버 시 파란색 */
}

/* 게시글 메뉴 */
.navbar-menu {
  display: flex;
  gap: 30px;
  margin-top: 10px; /* EduCinema 아래 간격 */
  justify-content: flex-start; /* 왼쪽 정렬 */
}

.navbar-menu a {
  color: #666; /* 메뉴 연한 회색 */
  text-decoration: none;
  font-size: 18px;
  font-weight: 500;
}

.navbar-menu a:hover {
  color: #0066FF; /* 파란색 강조 */
}
</style>

<template>
  <header>
    <nav>
      <!-- 로그인 상태에 따른 네비게이션 -->
      <div v-if="store.isLogin">
        <RouterLink :to="{ name: 'ArticleView' }">Articles</RouterLink> |
        <RouterLink :to="{ name: 'ProfileListView' }">Profiles</RouterLink> |
        <form @submit.prevent="logOut">
          <input type="submit" value="Logout">
        </form>
      </div>
      <div v-else>
        <RouterLink :to="{ name: 'SignUpView' }">SignUp</RouterLink> |
        <RouterLink :to="{ name: 'LogInView' }">LogIn</RouterLink>
      </div>
    </nav>
  </header>
  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore(); // Pinia 스토어

// 로그아웃 함수
const logOut = function () {
  store.logOut();
};
</script>

<style scoped>
:root {
  --primary-blue: #0066FF;
  --text-dark: #333333;
  --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Pretendard', sans-serif;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}
</style>

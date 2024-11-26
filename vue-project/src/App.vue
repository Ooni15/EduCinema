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
/* 스타일 추가 가능 */
</style>

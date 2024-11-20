<template>
  <div>
    <h1>회원가입 페이지</h1>
    <form @submit.prevent="signUp">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model.trim="username" required /><br>

      <label for="email">Email:</label>
      <input type="email" id="email" v-model.trim="email" required /><br>

      <label for="password1">Password:</label>
      <input type="password" id="password1" v-model.trim="password1" required /><br>

      <label for="password2">Password Confirmation:</label>
      <input type="password" id="password2" v-model.trim="password2" required /><br>

      <label for="major">Major:</label>
      <input type="text" id="major" v-model.trim="major" required /><br>

      <label for="bio">Bio:</label>
      <textarea id="bio" v-model="bio" placeholder="Write a short introduction..."></textarea><br>

      <label for="profile_picture">Profile Picture:</label>
      <input type="file" id="profile_picture" @change="handleFileUpload" /><br>

      <input type="submit" value="Sign Up" />
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

// 입력 필드 변수
const username = ref(null);
const email = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const major = ref(null);
const bio = ref(null);
const profile_picture = ref(null);

const store = useCounterStore();

// 파일 업로드 처리 함수
const handleFileUpload = (event) => {
  profile_picture.value = event.target.files[0];
};

// 회원가입 요청 함수
const signUp = () => {
  const payload = {
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    major: major.value,
    bio: bio.value,
    profile_picture: profile_picture.value, // 파일 데이터 포함
  };
  store.signUp(payload); // Pinia 스토어의 signUp 액션 호출
};
</script>

<style>
/* 스타일은 필요에 따라 추가 */
</style>

<template>
  <div class="signup-container">
    <h1>Sign Up</h1>
    <form @submit.prevent="signUp" class="signup-form">
      <div class="input-group">
        <label for="username" class="sr-only">Username</label>
        <input
          type="text"
          id="username"
          v-model.trim="username"
          placeholder="Enter your username"
          class="input-field"
          required
        />
        <div class="underline"></div>
      </div>

      <div class="input-group">
        <label for="email" class="sr-only">Email</label>
        <input
          type="email"
          id="email"
          v-model.trim="email"
          placeholder="Enter your email"
          class="input-field"
          required
        />
        <div class="underline"></div>
      </div>

      <div class="input-group">
        <label for="password1" class="sr-only">Password</label>
        <input
          type="password"
          id="password1"
          v-model.trim="password1"
          placeholder="Enter your password"
          class="input-field"
          required
        />
        <div class="underline"></div>
      </div>

      <div class="input-group">
        <label for="password2" class="sr-only">Password Confirmation</label>
        <input
          type="password"
          id="password2"
          v-model.trim="password2"
          placeholder="Confirm your password"
          class="input-field"
          required
        />
        <div class="underline"></div>
      </div>

      <div class="input-group">
        <label for="major" class="sr-only">Major</label>
        <input
          type="text"
          id="major"
          v-model.trim="major"
          placeholder="Enter your major"
          class="input-field"
          required
        />
        <div class="underline"></div>
      </div>

      <div class="input-group">
        <label for="bio" class="sr-only">Bio</label>
        <textarea
          id="bio"
          v-model="bio"
          placeholder="Write a short introduction..."
          class="input-field"
        ></textarea>
        <div class="underline"></div>
      </div>

      <div class="input-group">
        <label for="profile_picture" class="custom-file-label">Choose a Profile Picture</label>
        <input
          type="file"
          id="profile_picture"
          @change="handleFileUpload"
          class="file-input"
        />
        <span class="file-name">{{ selectedFileName || "No file chosen" }}</span>
      </div>

      <button type="submit" class="signup-btn">Sign Up</button>
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
    profile_picture: profile_picture.value,
  };
  store.signUp(payload);
};
</script>

<style scoped>
/* 전체 페이지 배경색 및 여백 설정 */
body {
  margin: 0;
  background-color: #f9f9f9; /* NavBar와 동일한 배경색 */
}

.signup-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 60px); /* NavBar 높이만큼 뺌 */
  padding-top: 60px; /* NavBar 높이만큼 여백 추가 */
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 48px;
  font-weight: bold;
  color: #000;
  margin-bottom: 50px;
}

.signup-form {
  width: 100%;
  max-width: 400px;
}

.input-group {
  margin-bottom: 30px;
  position: relative;
}

.input-field {
  width: 100%;
  border: none;
  border-bottom: 2px solid #000;
  padding: 15px 0;
  font-size: 20px;
  color: #000;
  outline: none;
  background: none;
}

.input-field::placeholder {
  color: #aaa;
}

.underline {
  height: 2px;
  width: 100%;
  background-color: #000;
}

.custom-file-label {
  display: inline-block;
  padding: 10px 15px;
  background-color: #000;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
}

.custom-file-label:hover {
  background-color: #333;
}

.file-input {
  display: none; /* 기본 파일 입력 숨김 */
}

.file-name {
  display: block;
  margin-top: 10px;
  font-size: 14px;
  color: #666;
  font-style: italic;
}


.signup-btn {
  width: 100%;
  padding: 15px;
  font-size: 18px;
  font-weight: bold;
  color: #fff;
  background-color: #000;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
  border-radius: 5px;
}

.signup-btn:hover {
  background-color: #333;
}
</style>

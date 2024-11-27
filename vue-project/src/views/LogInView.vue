<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="logIn" class="login-form">
      <div class="input-group">
        <label for="username" class="sr-only">아이디</label>
        <input
          type="text"
          id="username"
          v-model.trim="username"
          placeholder="아이디를 입력해주세요."
          class="input-field"
        />
        <div class="underline"></div>
      </div>
      <div class="input-group">
        <label for="password" class="sr-only">비밀번호</label>
        <input
          type="password"
          id="password"
          v-model.trim="password"
          placeholder="비밀번호를 입력해주세요."
          class="input-field"
        />
        <div class="underline"></div>
      </div>
      <button type="submit" class="login-btn">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref('')
const password = ref('')

const store = useCounterStore()

const logIn = () => {
  const payload = {
    username: username.value,
    password: password.value
  }
  
  store.logIn(payload)
}
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 60px); /* NavBar 높이만큼 빼줌 */
  background-color: #f9f9f9; /* NavBar와 동일한 배경색 */
  font-family: Arial, sans-serif;
  margin-top: -20px; /* NavBar로 인한 내려간 여백을 보정 */
}

h1 {
  font-size: 48px;
  font-weight: bold;
  color: #000;
  margin-bottom: 50px;
}

.login-form {
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

.login-btn {
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

.login-btn:hover {
  background-color: #333;
}
</style>

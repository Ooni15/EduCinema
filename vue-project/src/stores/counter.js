import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000/api/v1'
  const token = ref(null)
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()

  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        // console.log(res.data)
        articles.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const signUp = async function (payload) {
    const { username, email, password1, password2, major, bio, profile_picture } = payload;
  
    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('password1', password1);
    formData.append('password2', password2);
    formData.append('major', major);
    formData.append('bio', bio);
    if (profile_picture) {
      formData.append('profile_picture', profile_picture);
    }
  
    try {
      const res = await axios({
        method: 'post',
        url: `${API_URL}/accounts/signup/`,
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('회원가입 성공:', res.data);
      const password = password1;
      await logIn({ username, password }); // 로그인 시도
      const userStore = useUserStore(); // User Store 호출
      await userStore.fetchUsers(); // 사용자 리스트 갱신
    } catch (err) {
      const errorMessage = err.response?.data || '회원가입에 실패했습니다.';
      alert(errorMessage);
    }
  };
  
  // 로그인 요청 액션
  const logIn = function (payload) {
    const { username, password } = payload;
  
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: { username, password },
    })
      .then((res) => {
        const receivedToken = res.data.token; // 받은 토큰
        const receivedUsername = res.data.username;
        console.log('받은 토큰:', receivedToken);
        token.value = receivedToken; // Vue 상태에 저장
        
        localStorage.setItem('token', receivedToken); // 로컬 스토리지에 저장
        localStorage.setItem('username', receivedUsername); // 사용자 이름 로컬 스토리지 저장
        console.log('토큰 저장 완료:', localStorage.getItem('token'));
        console.log('로그인 성공:', receivedToken);
        console.log('로그인 username:', receivedUsername)
        router.push({ name: 'ArticleView' }); // 페이지 이동
      })
      .catch((err) => {
        console.error('로그인 실패:', err.response?.data || err);
      });
  };
  
  
  
  // [추가기능] 로그아웃
  const logOut = function () {
    // console.log('받은 토큰:', receivedToken); // 서버에서 받은 토큰
    console.log('Pinia에 저장된 토큰:', token.value); // Pinia 상태에 저장된 토큰
    console.log('LocalStorage에 저장된 토큰:', localStorage.getItem('token')); // 로컬 스토리지 확인


    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`, // 로컬 스토리지의 토큰 사용
      },
    })
      .then(() => {
        token.value = null; // Vue 상태 초기화
        localStorage.removeItem('token'); // 로컬 스토리지 초기화
        router.push({ name: 'LogInView' }); // 로그인 페이지로 이동
        console.log('로그아웃 성공');
      })
      .catch((err) => {
        console.error('로그아웃 실패:', err.response?.data || err);
      });
  };
  
  return { articles, API_URL, getArticles, signUp, logIn, token, isLogin, logOut }
}, { persist: true })



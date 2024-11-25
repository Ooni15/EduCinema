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
      url: `${API_URL}/articles/`,
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
  //좋아요
  // 좋아요 토글 함수
  const toggleLike = async function (articleId) {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/articles/${articleId}/like/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      // 좋아요 토글 후 게시글 상세 정보를 다시 가져옵니다.
      return getArticleDetail(articleId)
    } catch (error) {
      console.error('좋아요 토글 실패:', error)
      throw error
    }
  }

  // 게시글 상세 정보 가져오기
  const getArticleDetail = async function (articleId) {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/articles/${articleId}/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      return response.data
    } catch (error) {
      console.error('게시글 상세 정보 가져오기 실패:', error)
      throw error
    }
  }
  // 댓글 작성
  const addComment = async function (articleId, content) {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/articles/${articleId}/comments/`,
        headers: {
          Authorization: `Token ${token.value}`
        },
        data: { content }
      })
      return response.data
    } catch (error) {
      console.error('댓글 작성 실패:', error)
      throw error
    }
  }

  // 댓글 수정
  const updateComment = async function (articleId, commentId, content) {
    try {
      const response = await axios({
        method: 'put',
        url: `${API_URL}/articles/${articleId}/comments/${commentId}/`,
        headers: {
          Authorization: `Token ${token.value}`
        },
        data: { content }
      })
      return response.data
    } catch (error) {
      console.error('댓글 수정 실패:', error)
      throw error
    }
  }

  // 댓글 삭제
  const deleteComment = async function (articleId, commentId) {
    try {
      await axios({
        method: 'delete',
        url: `${API_URL}/articles/${articleId}/comments/${commentId}/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
    } catch (error) {
      console.error('댓글 삭제 실패:', error)
      throw error
    }
  }
  // 회원가입 요청 액션
  // 이미지 파일 때문에 formdata로 전송함 => Json이 안되자나
  const signUp = function (payload) {
    const { username, email, password1, password2, major, bio, profile_picture } = payload;
  
    // FormData 생성
    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('password1', password1);
    formData.append('password2', password2);
    formData.append('major', major);
    formData.append('bio', bio);
    if (profile_picture) {
      formData.append('profile_picture', profile_picture); // 이미지 파일 추가
    }
  
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`, // URL 확인
      data: formData, // FormData 전송
      headers: {
        'Content-Type': 'multipart/form-data', // 파일 업로드를 처리하는 헤더
      },
    })
      .then((res) => {
        console.log('회원가입 성공:', res.data);
        const password = password1;
        logIn({ username, password }); // 회원가입 성공 후 로그인 시도
      })
      .catch((err) => {
        const errorMessage = err.response?.data || '회원가입에 실패했습니다.';
        alert(errorMessage); // 오류 메시지 출력
      });
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
        console.log('받은 토큰:', receivedToken);
        token.value = receivedToken; // Vue 상태에 저장
        
        localStorage.setItem('token', receivedToken); // 로컬 스토리지에 저장
        console.log('토큰 저장 완료:', localStorage.getItem('token'));
        console.log('로그인 성공:', receivedToken);
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
  
  return { articles, API_URL, getArticles, toggleLike, addComment, updateComment, deleteComment, getArticleDetail, signUp, logIn, token, isLogin, logOut }
}, { persist: true })



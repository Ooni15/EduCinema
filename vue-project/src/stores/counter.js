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

  // 사용자가 작성한 게시글 가져오기
const getArticlesByUser = async (userId) => {
  try {
    const response = await axios.get(`${API_URL}/articles/user/${userId}/articles/`, {
      headers: { Authorization: `Token ${token.value}` },
    });
    return response.data;
  } catch (error) {
    console.error('사용자 게시글 가져오기 실패:', error);
    throw error;
  }
};

const getCommentsByUser = async (userId) => {
  try {
    const response = await axios.get(`${API_URL}/user/${userId}/comments/`, {
      headers: { Authorization: `Token ${token.value}` },
    });
    return response.data;
  } catch (error) {
    console.error('사용자 댓글 가져오기 실패:', error);
    throw error;
  }
};


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
  // 영화 목록 가져오기
  const getMovies = async () => {
    try {
      const response = await axios.get(`${API_URL}/movies/`, {
        headers: { Authorization: `Token ${token.value}` }
      })
      return response.data
    } catch (error) {
      console.error('영화 목록 가져오기 실패:', error)
      throw error
    }
  }
  // 현재 로그인한 사용자 정보 가져오기
  const getCurrentUser = async function () {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/accounts/me/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      return response.data
    } catch (error) {
      console.error('사용자 정보 가져오기 실패:', error)
      throw error
    }
  }
  // 게시글 생성
  const createArticle = async (articleData) => {
    try {
      const formData = new FormData()
      
      // 일반 데이터 추가
      for (const [key, value] of Object.entries(articleData)) {
        if (key !== 'learning_material_url' && value !== null) {
          formData.append(key, value)
        }
      }
  
      // 파일 데이터 별도 처리
      if (articleData.learning_material_url) {
        formData.append('learning_material_url', articleData.learning_material_url)
      }
  
      const response = await axios({
        method: 'post',
        url: `${API_URL}/articles/`,
        data: formData,
        headers: {
          Authorization: `Token ${token.value}`,
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      if (error.response?.data) {
        console.error('서버 응답 에러:', error.response.data)
      }
      throw error
    }
  }
  // Update article
  const updateArticle = async (articleId, articleData) => {
    try {
      const formData = new FormData()
      
      // 일반 데이터 추가
      for (const [key, value] of Object.entries(articleData)) {
        if (key !== 'learning_material' && key !== 'learning_material_url' && value !== null) {
          formData.append(key, value)
        }
      }
  
      // 파일 데이터 처리
      if (articleData.learning_material instanceof File) {
        // 새로운 파일이 선택된 경우
        formData.append('learning_material', articleData.learning_material)
      } else if (articleData.learning_material_url) {
        // 기존 파일 유지
        formData.append('learning_material_url', articleData.learning_material_url)
      }
  
      const response = await axios({
        method: 'put',
        url: `${API_URL}/articles/${articleId}/`,
        data: formData,
        headers: {
          Authorization: `Token ${token.value}`,
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      if (error.response?.data) {
        console.error('서버 응답 에러:', error.response.data)
      }
      throw error
    }
  }

  // Delete article
  const deleteArticle = async (articleId) => {
    try {
      await axios.delete(`${API_URL}/articles/${articleId}/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
    } catch (error) {
      console.error('게시글 삭제 실패:', error)
      throw error
    }
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
  const addComment = async (articleId, content) => {
    try {
      const response = await axios.post(
        `${API_URL}/articles/${articleId}/comments/`,
        {
          content: content,
          article: articleId
        },
        {
          headers: {
            'Authorization': `Token ${token.value}`,
            'Content-Type': 'application/json'
          }
        }
      )
      return response.data
    } catch (error) {
      console.error('댓글 작성 실패:', error.response?.data || error)
      throw error
    }
  }
  // 댓글 수정
  const updateComment = async (articleId, commentId, content) => {
    try {
      const response = await axios.put(
        `${API_URL}/articles/${articleId}/comments/${commentId}/`,
        {
          content: content,
          article: articleId
        },
        {
          headers: {
            Authorization: `Token ${token.value}`,
            'Content-Type': 'application/json'
          }
        }
      )
      return response.data
    } catch (error) {
      console.error('댓글 수정 실패:', error.response?.data || error)
      throw error
    }
  }

  // 댓글 삭제
  const deleteComment = async (articleId, commentId) => {
    try {
      await axios.delete(
        `${API_URL}/articles/${articleId}/comments/${commentId}/`,
        {
          headers: {
            Authorization: `Token ${token.value}`
          }
        }
      )
    } catch (error) {
      console.error('댓글 삭제 실패:', error.response?.data || error)
      throw error
    }
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
        localStorage.removeItem('userId');  // userId도 제거
      })
      .catch((err) => {
        console.error('로그아웃 실패:', err.response?.data || err);
      });
  };
  
  return { articles, API_URL, getArticles, getMovies, createArticle, getCurrentUser, updateArticle, deleteArticle, toggleLike, addComment, updateComment, deleteComment, getArticleDetail,getArticlesByUser, signUp, logIn, token, isLogin, logOut, getCommentsByUser }
}, { persist: true })



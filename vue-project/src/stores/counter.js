import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

  const API_URL = 'http://127.0.0.1:8000'
  const token = ref('4b88add7eb532df1dd12b8344167b1a3afea6d62')           // 임시로 토큰 값을 넣어주겠슴다
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()
  // 영화 object
  export const useCounterStore = defineStore('counter', () => {
    // const articles = ref([{
    //   movie: {
    //     movie_title: '',
    //     movie_genre: '',
    //     poster: ''
    //   }
    // }])
  const articles = ref([])
  // 전체 게시글 조회
  const getArticles = async () => {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/api/v1/articles/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      // 응답 데이터 구조 확인을 위한 로그 추가
      console.log('API Response:', response.data)
      articles.value = response.data
    } catch (error) {
      console.error('게시글 목록 조회 실패:', error)
    }
  }

  // 게시글 생성
  const createArticle = async (articleData) => {
    const formData = new FormData()
    
    // 일반 데이터 추가
    formData.append('title', articleData.title)
    formData.append('content', articleData.content)
    formData.append('related_major', articleData.related_major)
    formData.append('technology_type', articleData.technology_type)
    formData.append('movie_description', articleData.movie_description)
    formData.append('short_description', articleData.short_description)
    formData.append('movie_id', articleData.movie_id)

    // 파일 데이터 추가
    if (articleData.learning_material) {
      formData.append('learning_material_url', articleData.learning_material)
    }

    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/api/v1/articles/`,
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Token ${token.value}`
        }
      })
      return response.data
    } catch (error) {
      console.error('게시글 작성 실패:', error)
      throw error
    }
  }

  // 게시글 상세 조회
  const getArticleDetail = async (articleId) => {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/api/v1/articles/${articleId}/`,
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Token ${token.value}`
        }
      })
      return response.data
    } catch (error) {
      console.error('게시글 상세 조회 실패:', error)
      throw error
    }
  }

  // 게시글 수정
  const updateArticle = async (articleId, articleData) => {
    try {
      // FormData 대신 일반 객체로 데이터 전송
      const response = await axios({
        method: 'put',
        url: `${API_URL}/api/v1/articles/${articleId}/`,
        data: {
          title: articleData.title,
          content: articleData.content,
          related_major: articleData.related_major,
          technology_type: articleData.technology_type
        },
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      return response.data
    } catch (error) {
      console.error('게시글 수정 실패:', error)
      throw error
    }
  }

  // 게시글 삭제
  const deleteArticle = async (articleId) => {
    try {
      await axios({
        method: 'delete',
        url: `${API_URL}/api/v1/articles/${articleId}/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
    } catch (error) {
      console.error('게시글 삭제 실패:', error)
      throw error
    }
  }

  // 댓글 작성
  const createComment = async (articleId, content) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/api/v1/articles/${articleId}/comments/`,
        data: {
          content: content,
          article: articleId
        },
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      // 댓글 작성 후 게시글 목록 새로고침
      await getArticles()
      return response.data
    } catch (error) {
      console.error('댓글 작성 실패:', error)
      throw error
    }
  }
  // 댓글 수정
  const updateComment = async (commentId, content, articleId) => {
    try {
      const response = await axios({
        method: 'put',
        url: `${API_URL}/api/v1/comments/${commentId}/`,
        data: {
          content: content,
          article: articleId
        },
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      await getArticles()
      return response.data
    } catch (error) {
      console.error('댓글 수정 실패:', error)
      throw error
    }
  }
  // 댓글 삭제
const deleteComment = async (commentId) => {
  try {
    await axios({
      method: 'delete',
      url: `${API_URL}/api/v1/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    await getArticles()
    return true
  } catch (error) {
    console.error('댓글 삭제 실패:', error)
    throw error
  }
}
  // 좋아요 토글
  const toggleLike = async (articleId) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/api/v1/articles/${articleId}/like/`,
        data: {
          article_id: articleId
        },
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      return response.data
    } catch (error) {
      console.error('좋아요 처리 실패:', error)
      throw error
    }
  }

  // 회원가입 요청 액션
  const signUp = function (payload) {
    // const username = payload.username
    // const password1 = payload.password1
    // const password2 = payload.password2
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then((res) => {
        // console.log(res)
        // console.log('회원가입 성공')
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 로그인 요청 액션
  const logIn = function (payload) {
    // const username = payload.username
    // const password1 = payload.password
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        token.value = res.data.key
        router.push({ name: 'ArticleView' })
        // console.log(res.data)
        // console.log('로그인 성공')
      })
      .catch((err) => {
        console.log(err)
      })
  }
  
  // [추가기능] 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        token.value = null
        router.push({ name: 'ArticleView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }
  return { articles, 
    API_URL, 
    getArticles,
    createArticle,
    getArticleDetail,
    updateArticle,
    deleteArticle,
    createComment,
    updateComment,
    deleteComment,
    toggleLike,
    signUp, 
    logIn, 
    token, 
    isLogin, 
    logOut }
}, { persist: true })

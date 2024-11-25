<template>
  <div class="article-detail">
    <!-- 게시글 정보 -->
    <div v-if="article" class="article-content">
      <h1>{{ article.title }}</h1>
      
      <!-- 작성자 정보 -->
      <div class="user-info">
        <h3>작성자 정보</h3>
        <p>작성자: {{ article.user.username }}</p>
        <p>전공: {{ article.user.major }}</p>
        <p>기술: {{ article.technology_type }}</p>
      </div>

      <!-- 영화 정보 -->
      <div class="movie-info">
        <h3>관련 영화</h3>
        <!-- <img :src="article.movie.poster" :alt="article.movie.movie_title"> -->
             <!-- store.API_URL과 poster 경로를 합쳐서 완전한 URL 생성 -->
        <img 
          v-if="article?.movie?.poster" 
          :src="getFullImageUrl(article.movie.poster)" 
          :alt="article.movie.movie_title"
        >
        <p>영화 제목: {{ article.movie.movie_title }}</p>
        <p>장르: {{ article.movie.movie_genre }}</p>
      </div>

      <!-- 게시글 본문 -->
      <div class="article-body">
        <h4>내용</h4>
        <p>{{ article.content }}</p>
        <h4>기술 설명</h4>
        <p>{{ article.movie_description }}</p>
        <p>작성일: {{ article.created_at }}</p>
        <p>수정일: {{ article.updated_at }}</p>
      </div>
      <hr>
      <!-- 학습 자료 -->
      <div v-if="article.learning_material_url" class="learning-material">
        <h4>학습 자료</h4>
        <a :href="article.learning_material_url" target="_blank" class="material-link">
          자료 다운로드
        </a>
      </div>
      <!-- 좋아요 섹션 -->
      <div class="likes-section">
        <button @click="handleLike" :class="{ 'liked': article.is_liked }">
        {{ article.is_liked ? '좋아요 취소' : '좋아요' }}
        </button>
        <span>좋아요 수: {{ article.likes_count }}</span>
      </div>
      <!-- 댓글 섹션 -->
      <div class="comments-section">
        <h3>댓글</h3>
        <!-- 댓글 작성 폼 -->
        <div class="comment-form">
          <textarea v-model="newComment" placeholder="댓글을 작성하세요"></textarea>
          <button @click="addComment">댓글 작성</button>
        </div>

        <!-- 댓글 목록 -->
        <div v-for="comment in article.comments" :key="comment.id" class="comment">
          <p>{{ comment.content }}</p>
          <p>작성자: {{ comment.username }}</p>
          <p>작성일: {{ comment.created_at }}</p>
          <div v-if="comment.username === currentUser">
            <button @click="editComment(comment)">수정</button>
            <button @click="deleteComment(comment.id)">삭제</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'

const store = useCounterStore()
const route = useRoute()
const article = ref(null)
const newComment = ref('')
const token = localStorage.getItem('token')
const currentUserId = ref(null) // 현재 로그인한 사용자 ID
// const currentUser = computed(() => store.token ? JSON.parse(atob(store.token.split('.')[1])).username : null)

// 게시글 상세 정보 가져오기
const fetchArticleDetail = async () => {
  try {
    article.value = await store.getArticleDetail(route.params.id)
  } catch (error) {
    console.error('게시글 상세 정보 가져오기 실패:', error)
  }
}

// 좋아요 처리
const handleLike = async () => {
  try {
    article.value = await store.toggleLike(route.params.id)
  } catch (error) {
    console.error('좋아요 처리 실패:', error)
  }
}

// 게시글 조회
onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/articles/${route.params.id}/`,
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then((res) => {
      article.value = res.data
      // 현재 사용자 ID 설정
      currentUserId.value = res.data.user.id
    })
    .catch((err) => {
      console.log(err)
    })
  fetchArticleDetail()
})
const getFullImageUrl = (posterPath) => {
  if (!posterPath) return ''
  // 이미 전체 URL인 경우
  if (posterPath.startsWith('http')) return posterPath
  // API_URL에서 api/v1 부분을 제외하고 베이스 URL만 사용
  const baseUrl = store.API_URL.replace('/api/v1', '')
  return `${baseUrl}${posterPath}`
}
// 댓글 작성
const addComment = async () => {
  try {
    const response = await store.addComment(route.params.id, newComment.value)
    article.value.comments.push(response)
    newComment.value = ''
  } catch (error) {
    console.error('댓글 작성 실패:', error)
  }
}

// 댓글 수정
const editComment = async (comment) => {
  const updatedContent = prompt('댓글을 수정하세요', comment.content)
  if (updatedContent) {
    try {
      const response = await store.updateComment(route.params.id, comment.id, updatedContent)
      const index = article.value.comments.findIndex(c => c.id === comment.id)
      article.value.comments[index] = response
    } catch (error) {
      console.error('댓글 수정 실패:', error)
    }
  }
}

// 댓글 삭제
const deleteComment = async (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    try {
      await store.deleteComment(route.params.id, commentId)
      article.value.comments = article.value.comments.filter(c => c.id !== commentId)
    } catch (error) {
      console.error('댓글 삭제 실패:', error)
    }
  }
}
</script>

<style>
.article-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.article-content {
  margin-bottom: 30px;
}

.user-info, .movie-info, .article-body {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
/* 기존 스타일 유지 */
.movie-info img {
  max-width: 300px;  /* 최대 너비 지정 */
  height: auto;      /* 비율 유지 */
  object-fit: cover; /* 이미지 비율 유지하며 영역 채우기 */
  border-radius: 8px; /* 모서리 둥글게 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
}

/* 반응형 디자인을 위한 미디어 쿼리 */
@media (max-width: 768px) {
  .movie-info img {
    max-width: 100%;
    margin: 0 auto;
  }
}
.likes-section {
  margin-top: 20px;
}

.likes-section button {
  padding: 10px 20px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.likes-section button.liked {
  background-color: #ff6b6b;
  color: white;
}

.likes-section span {
  margin-left: 10px;
}
.comments-section {
  margin-top: 30px;
}

.comment {
  padding: 10px;
  margin: 10px 0;
  border-bottom: 1px solid #eee;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-form textarea {
  width: 100%;
  min-height: 100px;
  margin-bottom: 10px;
}

button {
  padding: 5px 10px;
  margin-right: 5px;
  cursor: pointer;
}
</style>

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
      <!-- 수정 및 삭제 버튼 -->
      <div v-if="isAuthor" class="article-actions">
        <button @click="editArticle">수정</button>
        <button @click="deleteArticle">삭제</button>
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
          <textarea 
            v-model="commentContent"
            placeholder="댓글을 작성하세요"
            class="comment-textarea"
          ></textarea>
          <button @click="addComment">작성</button>
        </div>

        <!-- 댓글 목록 -->
        <div class="comments-list">
          <div v-for="comment in article.comments" :key="comment.id" class="comment">
            <!-- 댓글 작성자 정보 -->
            <div class="comment-header">
              <img :src="comment.user?.profile_picture || '/default-profile.png'" alt="프로필" class="comment-profile-pic">
              <span class="comment-username">{{ comment.username }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
          
            <!-- 댓글 내용 (수정 모드에 따라 다르게 표시) -->
            <div v-if="editingCommentId === comment.id" class="comment-edit-form">
              <textarea 
                v-model="editingContent" 
                class="edit-textarea"
              ></textarea>
              <div class="edit-buttons">
                <button @click="submitEdit(comment)" class="save-btn">저장</button>
                <button @click="cancelEdit" class="cancel-btn">취소</button>
              </div>
            </div>
            <p v-else class="comment-content">{{ comment.content }}</p>
          
            <!-- 댓글 작성자인 경우에만 수정/삭제 버튼 표시 -->
            <div v-if="isCommentAuthor(comment)" class="comment-actions">
              <button @click="startEdit(comment)" v-if="editingCommentId !== comment.id">수정</button>
              <button @click="deleteComment(comment.id)">삭제</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const store = useCounterStore()
const route = useRoute()
const article = ref(null)
const commentContent = ref('') // ref 추가
// const currentUserId = ref(null) // 현재 로그인한 사용자 ID
const currentUserId = localStorage.getItem('userId')
// const currentUser = computed(() => store.token ? JSON.parse(atob(store.token.split('.')[1])).username : null)

onMounted(async () => {
  try {
    article.value = await store.getArticleDetail(route.params.id)
  } catch (error) {
    console.error('게시글 상세 정보 가져오기 실패:', error)
  }
})
// 좋아요 처리
const handleLike = async () => {
  try {
    article.value = await store.toggleLike(route.params.id)
  } catch (error) {
    console.error('좋아요 처리 실패:', error)
  }
}
const isAuthor = computed(() => {
  const username = localStorage.getItem('username')
  return article.value && 
         article.value.user && 
         article.value.user.username === username
})
const editArticle = () => {
  router.push(`/articles/${article.value.id}/edit`)  // 직접 경로 지정
}

const deleteArticle = async () => {
  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    try {
      await store.deleteArticle(article.value.id)
      router.push('/')  // 직접 경로 지정
    } catch (error) {
      console.error('게시글 삭제 실패:', error)
    }
  }
}
const getFullImageUrl = (posterPath) => {
  if (!posterPath) return ''
  // 이미 전체 URL인 경우
  if (posterPath.startsWith('http')) return posterPath
  // API_URL에서 api/v1 부분을 제외하고 베이스 URL만 사용
  const baseUrl = store.API_URL.replace('/api/v1', '')
  return `${baseUrl}${posterPath}`
}
// 댓글
// 추가할 ref들
const editingCommentId = ref(null)
const editingContent = ref('')

// 날짜 포맷팅 함수
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('ko-KR')
}
// 댓글 작성
const addComment = async () => {
  if (!commentContent.value.trim()) {
    console.error('댓글 내용을 입력해주세요')
    return
  }
  
  try {
    const articleId = route.params.id
    await store.addComment(articleId, commentContent.value)
    commentContent.value = '' // 입력 필드 초기화
    article.value = await store.getArticleDetail(articleId) // 댓글 목록 새로고침
  } catch (error) {
    console.error('댓글 작성 중 오류 발생:', error)
  }
}
// 댓글 작성자 확인
const isCommentAuthor = (comment) => {
  const username = localStorage.getItem('username')
  return comment.username === username
}

// 댓글 수정 시작
const startEdit = (comment) => {
  editingCommentId.value = comment.id
  editingContent.value = comment.content
}

// 댓글 수정 취소
const cancelEdit = () => {
  editingCommentId.value = null
  editingContent.value = ''
}

// 댓글 수정 제출
const submitEdit = async (comment) => {
  if (!editingContent.value.trim()) return
  try {
    const articleId = route.params.id
    await store.updateComment(articleId, comment.id, editingContent.value)
    // 게시글 상세 정보 새로고침
    article.value = await store.getArticleDetail(articleId)
    // 수정 모드 종료
    cancelEdit()
  } catch (error) {
    console.error('댓글 수정 실패:', error)
  }
}

// 댓글 삭제
const deleteComment = async (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    try {
      await store.deleteComment(route.params.id, commentId)
      article.value = await store.getArticleDetail(route.params.id)
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
.comment-form textarea {
  width: 100%;
  min-height: 80px;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.comment-profile-pic {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.comment-edit-form {
  margin: 10px 0;
}

.edit-textarea {
  width: 100%;
  min-height: 60px;
  padding: 8px;
  margin-bottom: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.edit-buttons {
  display: flex;
  gap: 8px;
}

.save-btn, .cancel-btn {
  padding: 4px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.save-btn {
  background-color: #42b983;
  color: white;
}

.cancel-btn {
  background-color: #666;
  color: white;
}
</style>

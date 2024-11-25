<template>
  <div class="detail-page">
    <div class="hero-section">
      <div class="container">
        <h1>{{ article?.title }}</h1>
        <div class="meta-tags">
          <span class="tag">{{ article?.movie?.movie_genre }}</span>
          <span class="tag">{{ article?.technology_type }}</span>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="content-wrapper">
        <!-- 작성자 정보 카드 -->
        <div class="info-card author-card">
          <h3>작성자 정보</h3>
          <div class="author-info">
            <p class="author-name">{{ article?.user?.username }}</p>
            <p class="author-major">{{ article?.user?.major }}</p>
          </div>
        </div>

        <!-- 영화 정보 카드 -->
        <div class="info-card movie-card">
          <h3>관련 영화</h3>
          <div class="movie-content">
            <img 
              v-if="article?.movie?.poster" 
              :src="getFullImageUrl(article.movie.poster)" 
              :alt="article.movie.movie_title"
            >
            <div class="movie-details">
              <h4>{{ article?.movie?.movie_title }}</h4>
              <p>{{ article?.movie?.movie_genre }}</p>
              <p class="tech-type">{{ article?.technology_type }}</p>
            </div>
          </div>
        </div>

        <!-- 본문 내용 -->
        <div class="content-card">
          <div class="content-section">
            <h4>내용</h4>
            <p>{{ article?.content }}</p>
          </div>
          <div class="content-section">
            <h4>기술 설명</h4>
            <p>{{ article?.movie_description }}</p>
          </div>
          <div class="meta-info">
            <span>작성일: {{ formatDate(article?.created_at) }}</span>
            <span>수정일: {{ formatDate(article?.updated_at) }}</span>
          </div>
        </div>

        <!-- 학습 자료 -->
        <div v-if="article?.learning_material_url" class="material-card">
          <h4>학습 자료</h4>
          <a :href="article.learning_material_url" target="_blank" class="download-button">
            자료 다운로드
          </a>
        </div>

        <!-- 작성자 액션 버튼 -->
        <div v-if="isAuthor" class="action-buttons">
          <button @click="editArticle" class="edit-button">수정</button>
          <button @click="deleteArticle" class="delete-button">삭제</button>
        </div>

        <!-- 좋아요 섹션 -->
        <div class="like-section">
          <button @click="handleLike" :class="{ 'liked': article?.is_liked }">
            {{ article?.is_liked ? '좋아요 취소' : '좋아요' }}
          </button>
          <span>{{ article?.likes_count }} 명이 좋아합니다</span>
        </div>

        <!-- 댓글 섹션 -->
        <div class="comments-section">
          <h3>댓글</h3>
          <div class="comment-form">
            <textarea 
              v-model="commentContent" 
              placeholder="댓글을 작성하세요"
            ></textarea>
            <button @click="addComment">작성</button>
          </div>

          <div class="comments-list">
            <div v-for="comment in article?.comments" :key="comment.id" class="comment">
              <div class="comment-header">
                <img :src="comment.user?.profile_picture || '/default-profile.png'" alt="프로필">
                <span class="username">{{ comment.username }}</span>
                <span class="date">{{ formatDate(comment.created_at) }}</span>
              </div>

              <div v-if="editingCommentId === comment.id" class="edit-form">
                <textarea v-model="editingContent"></textarea>
                <div class="edit-actions">
                  <button @click="submitEdit(comment)" class="save">저장</button>
                  <button @click="cancelEdit" class="cancel">취소</button>
                </div>
              </div>
              <p v-else>{{ comment.content }}</p>

              <div v-if="isCommentAuthor(comment)" class="comment-actions">
                <button @click="startEdit(comment)">수정</button>
                <button @click="deleteComment(comment.id)">삭제</button>
              </div>
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

<style scoped>
.detail-page {
  background: #f8f9fa;
  min-height: 100vh;
}

.hero-section {
  background: linear-gradient(135deg, #0066ff, #0044cc);
  padding: 60px 0;
  color: white;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.content-wrapper {
  margin: -40px auto 40px;
}

.info-card, .content-card, .material-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.movie-card .movie-content {
  display: flex;
  gap: 24px;
}

.movie-card img {
  width: 200px;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
}

.meta-tags {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.tag {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
}

.like-section button {
  background: #f0f7ff;
  color: #0066ff;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.like-section button.liked {
  background: #0066ff;
  color: white;
}

.comments-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.comment-form textarea {
  width: 100%;
  min-height: 100px;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 16px;
  resize: vertical;
}

.action-buttons {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.edit-button, .delete-button {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.edit-button {
  background: #0066ff;
  color: white;
}

.delete-button {
  background: #ff4444;
  color: white;
}

@media (max-width: 768px) {
  .movie-card .movie-content {
    flex-direction: column;
  }

  .movie-card img {
    width: 100%;
    height: auto;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>
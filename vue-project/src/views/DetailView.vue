<template>
  <div class="detail-page">
    <!-- Hero Section -->
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
      <!-- 본문 내용 -->
      <section class="content-section">
        <h3>내용</h3>
        <p>{{ article?.content }}</p>
        <h3>기술 설명</h3>
        <p>{{ article?.movie_description }}</p>
      </section>

      <hr class="divider" />

      <!-- 학습 자료 -->
      <div v-if="article?.learning_material_url" class="material-card">
        <h4>학습 자료</h4>
        <p>{{ getFileName(article.learning_material_url) }}</p>
        <a
          :href="getFullFileUrl(article.learning_material_url)"
          :download="getFileName(article.learning_material_url)"
          class="download-button"
        >
          다운로드
        </a>
      </div>

      <hr class="divider" />

      <!-- 영화 정보 -->
      <section class="movie-section">
        <h3>관련 영화</h3>
        <div class="movie-content">
          <img
            v-if="article?.movie?.poster"
            :src="getFullImageUrl(article.movie.poster)"
            :alt="article.movie.movie_title"
            class="movie-poster"
          />
          <div class="movie-details">
            <h4>{{ article?.movie?.movie_title }}</h4>
            <p><strong>장르:</strong> {{ article?.movie?.movie_genre }}</p>
            <p><strong>줄거리:</strong> {{ article?.movie?.movie_synopsis }}</p>
            <p><strong>평점:</strong> {{ article?.movie?.movie_rating }} / 5.0</p>
            <p><strong>사용된 기술:</strong> {{ article?.movie?.technologies }}</p>
            <p class="tech-type"><strong>학습자료에서 사용할 기술:</strong> {{ article?.technology_type }}</p>
          </div>
        </div>
      </section>

      <hr class="divider" />

      <!-- 작성자 정보 -->
      <section class="meta-info">
        <p><strong>작성일:</strong> {{ formatDate(article?.created_at) }}</p>
        <p><strong>작성자:</strong> {{ article?.user?.username }} ({{ article?.user?.major }})</p>
        <p><strong>수정일:</strong> {{ formatDate(article?.updated_at) }}</p>
      </section>

      <!-- 게시글 수정/삭제 버튼 -->
      <div v-if="isAuthor" class="action-buttons">
        <button @click="editArticle" class="edit-button">게시글 수정</button>
        <button @click="deleteArticle" class="delete-button">게시글 삭제</button>
      </div>

      <hr class="divider" />

      <!-- 좋아요 -->
      <section class="like-section">
        <button @click="handleLike" :class="{ 'liked': article?.is_liked }">
          {{ article?.is_liked ? '좋아요 취소' : '좋아요' }}
        </button>
        <span>{{ article?.likes_count }} 명이 좋아합니다</span>
      </section>

      <hr class="divider" />

      <!-- 댓글 -->
      <section class="comments-section">
        <h3>댓글</h3>
        <div class="comment-form">
          <textarea
            v-model="commentContent"
            placeholder="댓글을 작성하세요"
            class="comment-textarea"
          ></textarea>
          <button @click="addComment" class="submit-comment">작성</button>
        </div>

        <div class="comments-list">
          <div v-for="comment in article?.comments" :key="comment.id" class="comment">
            <div class="comment-header">
              <span class="username">{{ comment.username }}</span>
              <span class="date">{{ formatDate(comment.created_at) }}</span>
            </div>

            <!-- 댓글 내용 및 수정 기능 -->
            <div v-if="editingCommentId === comment.id" class="edit-comment">
              <textarea v-model="editingContent" class="edit-textarea"></textarea>
              <div class="edit-actions">
                <button @click="submitEdit(comment)" class="save-comment">저장</button>
                <button @click="cancelEdit" class="cancel-edit">취소</button>
              </div>
            </div>
            <p v-else>{{ comment.content }}</p>

            <!-- 댓글 수정/삭제 버튼 -->
            <div v-if="isCommentAuthor(comment)" class="comment-actions">
              <button @click="startEdit(comment)" class="edit-comment-btn">수정</button>
              <button @click="deleteComment(comment.id)" class="delete-comment-btn">삭제</button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
/* 전체 페이지 */
body {
  font-family: 'Arial', sans-serif;
  background-color: #f9f9f9;
  color: #333;
  margin: 0;
}

.detail-page {
  width: 100%;
  padding: 20px 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Hero Section */
.hero-section {
  background-color:  #f1f3f5;
  color:   #333;;
  text-align: center;
  padding: 40px 20px;
}

.hero-section h1 {
  font-size: 2rem;
  margin: 0;
}

.meta-tags {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}

.tag {
  background: #333;
  color: #fff;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
}

/* 섹션 스타일 */
section {
  margin: 20px 0;
}

h3 {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

p {
  line-height: 1.6;
  margin-bottom: 10px;
  color: #555;
}

/* 구분선 */
.divider {
  border: none;
  border-top: 1px solid #ccc;
  margin: 20px 0;
}

/* 영화 섹션 */
.movie-content {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.movie-poster {
  width: 120px;
  height: 180px;
  object-fit: cover;
}

.movie-details strong {
  color: #333;
  margin-right: 5px;
}

.tech-type {
  margin-top: 10px;
  color: #666;
}

/* 좋아요 버튼 */
.like-section {
  text-align: center;
  margin-top: 20px;
}

.like-section button {
  background: #333;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.like-section button:hover {
  background: #666;
}

.like-section span {
  display: block;
  margin-top: 10px;
  color: #666;
}

/* 댓글 섹션 */
.comments-section {
  margin-top: 20px;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.comment-textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.submit-comment {
  background: #000;
  color: #fff;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-comment:hover {
  background: #333;
}

.comments-list .comment {
  padding: 10px 0;
  border-bottom: 1px solid #ccc;
}

.comment-header {
  font-size: 0.9rem;
  color: #666;
}

/* 수정/삭제 버튼 */
.action-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.edit-button,
.delete-button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
}

.edit-button {
  background: #333;
  color: #fff;
}

.edit-button:hover {
  background: #666;
}

.delete-button {
  background: #666;
  color: #fff;
}

.delete-button:hover {
  background: #cc0000;
}

/* 댓글 수정 기능 */
.edit-comment {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.edit-textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.edit-actions {
  display: flex;
  gap: 10px;
}

.save-comment {
  background: #333;
  color: #fff;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.save-comment:hover {
  background: #666;
}

.cancel-edit {
  background: #ccc;
  color: #000;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.cancel-edit:hover {
  background: #aaa;
}

/* 댓글 수정/삭제 버튼 */
.comment-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 5px;
}

.edit-comment-btn {
  background: #333;
  color: #fff;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.edit-comment-btn:hover {
  background: #666;
}

.delete-comment-btn {
  background: #ccc;
  color: #000;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.delete-comment-btn:hover {
  background: #aaa;
}

</style>


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
// GPT 챗봇 관련 상태 추가
const chatMessages = ref([])
const userQuery = ref('')
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
// 파일이요
const getFileName = (filePath) => {
  if (!filePath) return ''
  // URL에서 파일명만 추출
  const fileName = filePath.split('/').pop()
  // URL 디코딩하여 한글 복원
  return decodeURIComponent(fileName)
}
const getFullFileUrl = (filePath) => {
  if (!filePath) return ''
  if (filePath.startsWith('http')) return filePath
  const baseUrl = store.API_URL.replace('/api/v1', '')
  return `${baseUrl}${filePath}`
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
//chat-bot
const sendGptQuery = async () => {
  if (!userQuery.value.trim()) return
  
  chatMessages.value.push({ role: 'user', content: userQuery.value })
  
  try {
    const token = localStorage.getItem('token')
    const response = await axios.post(
      `${store.API_URL}/articles/${route.params.id}/gpt-query/`, 
      { user_query: userQuery.value },
      {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    
    chatMessages.value.push({ role: 'assistant', content: response.data.answer })
  } catch (error) {
    console.error('GPT 쿼리 오류:', error)
    chatMessages.value.push({ 
      role: 'assistant', 
      content: '죄송합니다. 오류가 발생했습니다.' 
    })
  }
  
  userQuery.value = ''
}
</script>
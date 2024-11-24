<template>
  <div class="article-detail">
    <!-- 게시글 헤더 -->
    <div class="article-header">
      <h2>{{ article.title }}</h2>
      <div class="article-meta">
        <div class="user-info">
          <img 
            :src="article.user?.profile_picture || '/default-profile.png'" 
            alt="프로필 사진"
            class="profile-pic"
          >
          <span class="username">{{ article.user?.username }}</span>
          <span class="major">{{ article.user?.major }}</span>
        </div>
        <div class="post-info">
          <!-- <span>작성일: {{ formatDate(article.created_at) }}</span> -->
          <span>최종 수정일: {{ formatDate(article.updated_at) }}</span>
        </div>
      </div>
    </div>

    <!-- 영화 정보 -->
    <div class="article-card">
    <div class="movie-info">
      <img
        v-if="article?.movie"
        :src="getImageUrl(article.movie.poster)"
        :alt="article.movie.movie_title"
        class="movie-poster"
      >
      <div class="movie-details">
        <h4>Movie Title: {{ article?.movie?.movie_title }}</h4>
        <p>Movie Genre: {{ article?.movie?.movie_genre }}</p>
      </div>
    </div>
  </div>
    <!-- 게시글 본문 -->
    <div class="article-content">
      <div class="tech-info">
        <h4>기술 정보</h4>
        <p>관련 전공: {{ article.related_major }}</p>
        <p>기술 분야: {{ article.technology_type }}</p>
      </div>
      
      <div class="description">
        <h4>기술 설명</h4>
        <p>{{ article.movie_description }}</p>
      </div>

      <div class="main-content">
        <h4>내용</h4>
        <p>{{ article.content }}</p>
      </div>

      <!-- 학습 자료 -->
      <div v-if="article.learning_material_url" class="learning-material">
        <h4>학습 자료</h4>
        <a :href="article.learning_material_url" target="_blank" class="material-link">
          자료 다운로드
        </a>
      </div>
    </div>

    <!-- 좋아요 섹션 -->
    <div class="likes-section">
      <button @click="handleLike" class="like-button" :class="{ 'liked': article.is_liked }">
        ❤️ {{ article.likes_count }}
      </button>
    </div>

    <!-- 댓글 섹션 -->
    <div class="comments-section">
      <h3>댓글</h3>
      <!-- 댓글 작성 폼 -->
      <div class="comment-form">
        <textarea v-model="newComment" placeholder="댓글을 작성하세요"></textarea>
        <button @click="submitComment">작성</button>
      </div>

      <!-- 댓글 목록 -->
      <div class="comments-list">
        <div v-for="comment in article.comments" :key="comment.id" class="comment">
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
              @keyup.enter="submitEdit(comment)"
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
            <button @click="deleteComment(comment)">삭제</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 게시글 작성자인 경우 수정/삭제 버튼 -->
    <div v-if="isAuthor" class="article-actions">
      <button @click="handleEdit" class="edit-btn">수정</button>
      <button @click="handleDelete" class="delete-btn">삭제</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const article = ref({})
const newComment = ref('')

const props = defineProps({
  article: {
    type: Object,
    required: true,
    default: () => ({
      movie: {
        movie_title: '',
        movie_genre: '',
        poster: ''
      }
    })
  }
})

const getImageUrl = (poster) => {
  return poster || '/default-movie-poster.jpg'
}
// 날짜 포맷팅
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('ko-KR')
}

// 작성자 여부 확인
const isAuthor = computed(() => {
  return store.token && article.value.user?.id === store.userId
})

// 댓글 작성자 여부 확인
const isCommentAuthor = (comment) => {
  return store.token && comment.user?.id === store.userId
}

onMounted(async () => {
  try {
    const response = await store.getArticleDetail(route.params.id)
    article.value = response
  } catch (error) {
    console.error('게시글 로딩 실패:', error)
  }
})

// 좋아요 처리
const handleLike = async () => {
  try {
    await store.toggleLike(article.value.id)
    const response = await store.getArticleDetail(route.params.id)
    article.value = response
  } catch (error) {
    console.error('좋아요 처리 실패:', error)
  }
}

// 댓글 작성
const submitComment = async () => {
  if (!newComment.value.trim()) return
  
  try {
    await store.createComment(article.value.id, newComment.value)
    newComment.value = ''
    const response = await store.getArticleDetail(route.params.id)
    article.value = response
  } catch (error) {
    console.error('댓글 작성 실패:', error)
  }
}
// 댓글 수정 관련 상태 추가
const editingCommentId = ref(null)
const editingContent = ref('')

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
    await store.updateComment(comment.id, editingContent.value, article.value.id)
    // 게시글 상세 정보 새로고침
    const response = await store.getArticleDetail(route.params.id)
    article.value = response
    // 수정 모드 종료
    cancelEdit()
  } catch (error) {
    console.error('댓글 수정 실패:', error)
  }
}

// 댓글 삭제
const deleteComment = async (comment) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    try {
      await store.deleteComment(comment.id, article.value.id)  // article.id 추가
      // 게시글 상세 정보 새로고침
      const response = await store.getArticleDetail(route.params.id)
      article.value = response
    } catch (error) {
      console.error('댓글 삭제 실패:', error)
    }
  }
}

// 게시글 수정
const handleEdit = () => {
  router.push({ 
    name: 'EditView', 
    params: { id: article.value.id }
  })
}

// 게시글 삭제
const handleDelete = async () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    try {
      await store.deleteArticle(article.value.id)
      router.push({ name: 'ArticleView' })
    } catch (error) {
      console.error('삭제 실패:', error)
    }
  }
}
</script>

<style scoped>
.article-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.article-header {
  margin-bottom: 30px;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}
.article-card {
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.movie-info {
  display: flex;
  gap: 1rem;
}

.movie-poster {
  width: 120px;
  height: 180px;
  object-fit: cover;
  border-radius: 4px;
}

.movie-details {
  flex: 1;
}

.likes-section {
  margin: 20px 0;
}

.like-button {
  padding: 8px 16px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
}

.like-button.liked {
  background-color: #ff4444;
  color: white;
}

.comments-section {
  margin-top: 30px;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-form textarea {
  width: 100%;
  min-height: 80px;
  margin-bottom: 10px;
  padding: 8px;
}

.comment {
  padding: 10px;
  border-bottom: 1px solid #eee;
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
.article-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.edit-btn, .delete-btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.edit-btn {
  background-color: #42b983;
  color: white;
}

.delete-btn {
  background-color: #ff4444;
  color: white;
}
</style>
<template>
  <div class="edit-page">
    <div class="hero-section">
      <div class="container">
        <h1>학습자료 수정</h1>
      </div>
    </div>

    <div class="container">
      <div class="form-container">
        <form @submit.prevent="submitUpdate" class="edit-form">
          <div class="form-group">
            <label for="title">제목</label>
            <input 
              type="text" 
              id="title" 
              v-model.trim="article.title" 
              required
              placeholder="제목을 입력하세요"
            >
          </div>

          <div class="form-group">
            <label for="movie">영화 선택</label>
            <select id="movie" v-model="article.movie" required>
              <option value="" disabled>영화를 선택하세요</option>
              <option v-for="movie in movies" :key="movie.id" :value="movie.id">
                {{ movie.movie_title }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="related_major">관련 전공</label>
            <input 
              type="text" 
              id="related_major" 
              v-model.trim="article.related_major" 
              required
              placeholder="예: 전자공학"
            >
          </div>

          <div class="form-group">
            <label for="technology_type">관련 기술</label>
            <input 
              type="text" 
              id="technology_type" 
              v-model.trim="article.technology_type" 
              required
              placeholder="예: AI 기술"
            >
          </div>

          <div class="form-group">
            <label for="content">내용</label>
            <textarea 
              id="content" 
              v-model.trim="article.content" 
              required
              placeholder="내용을 입력하세요"
              rows="6"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="movie_description">기술 설명</label>
            <textarea 
              id="movie_description" 
              v-model.trim="article.movie_description" 
              required
              placeholder="영화에 사용된 기술에 대해 설명해주세요"
              rows="4"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="learning_material_url">학습 자료</label>
            <div class="file-upload">
              <input 
                type="file" 
                id="learning_material_url" 
                @change="handleFileUpload"
                class="file-input"
              >
              <label for="learning_material_url" class="file-label">
                파일 선택
              </label>
              <span v-if="article.learning_material_url" class="current-file">
                현재 파일: {{ article.learning_material_url }}
              </span>
            </div>
          </div>

          <div class="button-group">
            <button type="submit" class="submit-button">수정 완료</button>
            <button type="button" @click="goBack" class="cancel-button">취소</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 페이지 전체 스타일 */
.edit-page {
  min-height: 100vh;
  background: #f8f9fa;
}

/* Hero Section */
.hero-section {
  /* background-color: #000;
  color: white; */
  background-color:  #f1f3f5;
  color:   #333;
  text-align: center;
  padding: 40px 20px;
  margin-bottom: 40px;
}

.hero-section h1 {
  font-size: 1.8rem;
  margin: 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 폼 스타일 */
.form-container {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

input, select, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input:focus, select:focus, textarea:focus {
  border-color: #000;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

textarea {
  resize: vertical;
  min-height: 100px;
}

/* 파일 업로드 스타일 */
.file-upload {
  position: relative;
}

.file-input {
  opacity: 0;
  position: absolute;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-label {
  display: inline-block;
  padding: 10px 20px;
  background: #000;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s;
}

.file-label:hover {
  background-color: #333;
}

.current-file {
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}

/* 버튼 스타일 */
.button-group {
  display: flex;
  gap: 16px;
  margin-top: 20px;
}

.submit-button {
  flex: 1;
  background: #000;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s, transform 0.2s;
}

.submit-button:hover {
  background: #333;
  transform: translateY(-2px);
}

.cancel-button {
  flex: 1;
  background: #000;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.cancel-button:hover {
  background: #333;
  transform: translateY(-2px);
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .button-group {
    flex-direction: column;
    gap: 10px;
  }

  .form-container {
    padding: 20px;
  }
}
</style>


<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute, useRouter } from 'vue-router'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const movies = ref([])
const article = ref({
  title: '',
  movie: null,
  related_major: '',
  technology_type: '',
  content: '',
  movie_description: '',
  learning_material_url: null
})

onMounted(async () => {
  try {
    // 영화 목록 가져오기
    movies.value = await store.getMovies()
    // 게시글 상세 정보 가져오기
    const articleData = await store.getArticleDetail(route.params.id)
    article.value = {
      ...articleData,
      movie: articleData.movie.id
    }
  } catch (error) {
    console.error('데이터 가져오기 실패:', error)
  }
})

const handleFileUpload = (event) => {
  article.value.learning_material_url = event.target.files[0]
}

const submitUpdate = async () => {
  try {
    await store.updateArticle(route.params.id, article.value)
    router.push(`/articles/${route.params.id}`)
  } catch (error) {
    console.error('게시글 수정 실패:', error)
  }
}

const goBack = () => {
  router.go(-1)
}
</script>
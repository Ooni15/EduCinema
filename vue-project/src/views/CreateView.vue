<template>
  <div class="create-page">
    <div class="hero-section">
      <div class="container">
        <h1>새로운 게시글 작성</h1>
      </div>
    </div>
    <div class="container">
      <div class="form-container">
        <form @submit.prevent="submitArticle" class="create-form">
          <div class="form-group">
            <label for="title">제목</label>
            <input 
              type="text" 
              id="title" 
              v-model.trim="article.title" 
              required
              placeholder="게시글 제목을 입력하세요"
            >
          </div>

          <div class="form-group">
            <label for="movie">영화 선택</label>
            <select id="movie" v-model="article.movie" required>
              <option value="" disabled selected>영화를 선택하세요</option>
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
              placeholder="예: 비행 제어"
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
            <label for="learning_material_url">학습 자료 (PDF, PPT만 가능)</label>
            <div class="file-upload">
              <input 
                type="file" 
                id="learning_material_url" 
                @change="handleFileUpload"
                accept=".pdf,.ppt,.pptx"
                class="file-input"
              >
              <label for="learning_material_url" class="file-label">
                {{ uploadFileName || '파일 선택' }}
              </label>
            </div>
          </div>

          <div class="form-group">
            <label for="movie_description">한 줄 소개</label>
            <input 
              type="text" 
              id="movie_description" 
              v-model.trim="article.movie_description"
              placeholder="첨부파일에 대한 간단한 소개를 작성하세요"
            >
          </div>
          <button type="submit" class="submit-button">게시글 작성 완료</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
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
    movies.value = await store.getMovies()
  } catch (error) {
    console.error('영화 목록 가져오기 실패:', error)
  }
})

const uploadFileName = ref('')

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const fileExt = file.name.split('.').pop().toLowerCase()
    if (['pdf', 'ppt', 'pptx'].includes(fileExt)) {
      article.value.learning_material_url = file
      uploadFileName.value = file.name
    } else {
      alert('PDF 또는 PPT 파일만 업로드 가능합니다.')
      event.target.value = ''
    }
  }
}
const submitArticle = async () => {
  try {
    await store.createArticle(article.value)
    router.push({ name: 'ArticleView' })
  } catch (error) {
    console.error('게시글 작성 실패:', error)
  }
}
</script>

<style scoped>
.create-page {
  min-height: 100vh;
  background: #f8f9fa;
}

.hero-section {
  background: linear-gradient(135deg, #0066ff, #0044cc);
  padding: 20px 0;
  color: white;
  margin-bottom: 20px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.form-container {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 40px;
}

.form-group {
  margin-bottom: 24px;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

input, select, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #0066ff;
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}

textarea {
  resize: vertical;
  min-height: 120px;
}

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
  padding: 12px 24px;
  background: #f0f7ff;
  color: #0066ff;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-label:hover {
  background: #e0f0ff;
}

.submit-button {
  width: 30%;
  padding: 16px;
  background: #0066ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background: #0052cc;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .form-container {
    padding: 20px;
  }
  
  .container {
    padding: 0 16px;
  }
}
</style>

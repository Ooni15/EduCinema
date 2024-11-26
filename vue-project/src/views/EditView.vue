<template>
  <div class="edit-page">
    <div class="hero-section">
      <div class="container">
        <h1>게시글 수정</h1>
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
  
  <style scoped>
  .edit-page {
    min-height: 100vh;
    background: #f8f9fa;
  }
  
  .hero-section {
    background: linear-gradient(135deg, #0066ff, #0044cc);
    padding: 40px 0;
    color: white;
    margin-bottom: 40px;
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
  
  .current-file {
    display: block;
    margin-top: 8px;
    font-size: 14px;
    color: #666;
  }
  
  .button-group {
    display: flex;
    gap: 16px;
    margin-top: 32px;
  }
  
  .submit-button, .cancel-button {
    flex: 1;
    padding: 16px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .submit-button {
    background: #0066ff;
    color: white;
  }
  
  .submit-button:hover {
    background: #0052cc;
    transform: translateY(-2px);
  }
  
  .cancel-button {
    background: #f8f9fa;
    color: #666;
    border: 1px solid #e0e0e0;
  }
  
  .cancel-button:hover {
    background: #e9ecef;
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
    
    .button-group {
      flex-direction: column;
    }
  }
  </style>
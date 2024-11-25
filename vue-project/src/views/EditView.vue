<template>
    <div class="edit-form">
      <h1>게시글 수정</h1>
      <form @submit.prevent="submitUpdate">
        <div class="form-group">
          <label for="title">제목:</label>
          <input type="text" id="title" v-model.trim="article.title" required>
        </div>
  
        <div class="form-group">
          <label for="movie">영화:</label>
          <select id="movie" v-model="article.movie" required>
            <option v-for="movie in movies" :key="movie.id" :value="movie.id">
              {{ movie.movie_title }}
            </option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="related_major">전공:</label>
          <input type="text" id="related_major" v-model.trim="article.related_major" required>
        </div>
  
        <div class="form-group">
          <label for="technology_type">기술:</label>
          <input type="text" id="technology_type" v-model.trim="article.technology_type" required>
        </div>
  
        <div class="form-group">
          <label for="content">내용:</label>
          <textarea id="content" v-model.trim="article.content" required></textarea>
        </div>
  
        <div class="form-group">
          <label for="movie_description">기술 설명:</label>
          <textarea id="movie_description" v-model.trim="article.movie_description" required></textarea>
        </div>
  
        <div class="form-group">
          <label for="learning_material">학습 자료:</label>
          <input type="file" id="learning_material" @change="handleFileUpload">
          <span v-if="article.learning_material_url">현재 파일: {{ article.learning_material_url }}</span>
        </div>
  
        <div class="button-group">
          <button type="submit" class="submit-btn">수정 완료</button>
          <button type="button" @click="goBack" class="cancel-btn">취소</button>
        </div>
      </form>
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
    learning_material: null
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
    article.value.learning_material = event.target.files[0]
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
  .edit-form {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input[type="text"],
  select,
  textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  textarea {
    min-height: 150px;
  }
  
  .button-group {
    margin-top: 20px;
  }
  
  button {
    padding: 10px 20px;
    margin-right: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .submit-btn {
    background-color: #4CAF50;
    color: white;
  }
  
  .cancel-btn {
    background-color: #f44336;
    color: white;
  }
  </style>
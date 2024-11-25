<template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="submitArticle">
      <div>
        <label for="title">제목:</label>
        <input type="text" id="title" v-model.trim="article.title" required>
      </div>
      <div>
        <label for="movie">영화:</label>
        <select id="movie" v-model="article.movie" required>
          <option v-for="movie in movies" :key="movie.id" :value="movie.id">
            {{ movie.movie_title }}
          </option>
        </select>
      </div>
      <div>
        <label for="related_major">전공:</label>
        <input type="text" id="related_major" v-model.trim="article.related_major" required>
      </div>
      <div>
        <label for="technology_type">기술:</label>
        <input type="text" id="technology_type" v-model.trim="article.technology_type" required>
      </div>
      <div>
        <label for="content">내용:</label>
        <textarea id="content" v-model.trim="article.content" required></textarea>
      </div>
      <div>
        <label for="movie_description">한 줄 소개:</label>
        <input type="text" id="movie_description" v-model.trim="article.movie_description">
      </div>
      <div>
        <label for="learning_material">학습 자료:</label>
        <input type="file" id="learning_material" @change="handleFileUpload">
      </div>
      <button type="submit">게시글 작성</button>
    </form>
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
  related_major: '전자공학',
  technology_type: '비행 제어',
  content: '',
  movie_description: '',
  learning_material: null
})

onMounted(async () => {
  try {
    movies.value = await store.getMovies()
  } catch (error) {
    console.error('영화 목록 가져오기 실패:', error)
  }
})

const handleFileUpload = (event) => {
  article.value.learning_material = event.target.files[0]
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
</style>

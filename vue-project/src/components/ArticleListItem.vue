<template>
  <div class="article-card">
    <RouterLink 
      :to="{ name: 'DetailView', params: { id: article.id } }"
      class="article-link"
    >
      <div class="content-wrapper">
        <div class="poster-container">
          <img 
            :src="getMoviePoster(article.movie?.poster)"
            :alt="article.movie?.movie_title"
            class="movie-poster"
          >
        </div>
        <div class="article-info">
          <h3 class="article-title">{{ article.title }}</h3>
          <div class="meta-wrapper">
            <span class="author">{{ article.user?.username }}</span>
          </div>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

const props = defineProps({
  article: Object
})

const getMoviePoster = (posterPath) => {
  if (!posterPath) return '/default-movie-poster.jpg'
  if (posterPath.startsWith('http')) return posterPath
  const baseUrl = store.API_URL.replace('/api/v1', '')
  return `${baseUrl}${posterPath}`
}
</script>

<style scoped>
.article-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  width: 100%; /* 카드 크기를 그리드에 맞춤 */
  max-width: 400px; /* 최대 가로 크기 */
  height: 350px; /* 일정한 높이 */
}

.article-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.poster-container {
  flex: 2;
  background: #f5f5f5;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-info {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.article-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.meta-wrapper {
  font-size: 14px;
  color: #666;
}

.action-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  font-size: 14px;
  font-weight: bold;
  text-align: center;
  border-radius: 5px;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #0056b3;
}
</style>



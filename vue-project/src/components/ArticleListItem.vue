<template>
  <div class="article-card">
    <RouterLink 
      :to="{ name: 'DetailView', params: { id: article.id } }"
      class="article-link"
    >
      <div class="poster-container">
        <img 
          :src="getMoviePoster(article.movie?.poster)"
          :alt="article.movie?.movie_title"
          class="movie-poster"
        >
      </div>
      <div class="article-info">
        <h3 class="article-title">{{ article.title }}</h3>
        <p class="article-meta">{{ article.user?.username }}</p>
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
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  background: white;
}

.article-card:hover {
  transform: translateY(-5px);
}

.article-link {
  text-decoration: none;
  color: inherit;
}

.poster-container {
  position: relative;
  padding-top: 150%; /* 2:3 비율 유지 */
}

.movie-poster {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-info {
  padding: 12px;
}

.article-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.article-meta {
  margin: 4px 0 0;
  font-size: 0.875rem;
  color: #666;
}
</style>
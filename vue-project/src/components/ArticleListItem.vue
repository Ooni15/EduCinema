//ArticleListItem.vue
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
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  height: 100%;
}

.article-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.15);
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.article-link {
  text-decoration: none;
  color: inherit;
  display: block;
  height: 100%;
}

.poster-container {
  position: relative;
  padding-top: 140%;
  background: #f5f5f5;
}

.movie-poster {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.article-info {
  padding: 20px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tags {
  display: flex;
  gap: 8px;
}

.tag {
  background: #f0f7ff;
  color: #0066ff;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.article-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta-wrapper {
  margin-top: auto;
}

.author {
  color: #666;
  font-size: 14px;
  font-weight: 500;
}
</style>
<template>
  <div class="article-card">
    <div class="movie-info">
      <img 
      v-if="article.movie"
      :src="getImageUrl(article.movie.poster)" 
      :alt="article.movie.movie_title"
      class="movie-poster"
      >
      <div class="movie-details">
        <h4>Movie Title: {{ article.movie?.movie_title }}</h4>
        <p>Movie Genre: {{ article.movie?.movie_genre }}</p>
      </div>
    </div>

    <div class="article-content">
      <h3 class="article-title">{{ article.title }}</h3>
      <p class="article-description">{{ article.content }}</p>
      
      <div class="tech-info">
        <span class="tech-tag">{{ article.technology_type }}</span>
        <span class="major-tag">{{ article.related_major }}</span>
      </div>

      <div class="user-info">
        <div class="user-profile">
          <img 
            :src="article.user?.profile_picture || '/default-profile.png'" 
            alt="프로필 사진"
            class="profile-pic"
          >
          <span>{{ article.user?.username }}</span>
        </div>
        <div class="post-meta">
          <span class="likes-count">❤️ {{ article.likes_count }}</span>
          <span class="comments-count">💬 {{ article.comments_count }}</span>
          <!-- /comments 개수가 올바르게 조회되는지 확인 필요함 -->
        </div>
      </div>
    </div>

    <div class="article-footer">
      <RouterLink 
        :to="{ name: 'DetailView', params: { id: article.id } }"
        class="detail-link"
      >
        자세히 보기
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ko-KR')
}

</script>

<style scoped>
.article-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 15px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.movie-info {
  display: flex;
  gap: 15px;
}

.movie-poster {
  width: 120px;
  height: 180px;
  object-fit: cover;
  border-radius: 4px;
}

.movie-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.article-title {
  font-size: 1.4em;
  margin: 10px 0;
  color: #2c3e50;
}

.article-description {
  color: #666;
  margin-bottom: 15px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.tech-info {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.tech-tag, .major-tag {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
}

.tech-tag {
  background-color: #e3f2fd;
  color: #1976d2;
}

.major-tag {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-top: 1px solid #eee;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
}

.profile-pic {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
}

.post-meta {
  display: flex;
  gap: 15px;
  color: #666;
  font-size: 0.9em;
}

.detail-link {
  display: inline-block;
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  text-align: center;
  transition: background-color 0.2s;
}

.detail-link:hover {
  background-color: #3aa876;
}

.likes-count, .comments-count {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
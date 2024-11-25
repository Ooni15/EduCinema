<template>
  <div class="article-page">
    <div class="hero-section">
      <div class="container">
        <div class="header-content">
          <h1>게시글 조회</h1>
          <RouterLink :to="{ name: 'CreateView' }" class="create-button">
            게시글 작성하기
          </RouterLink>
        </div>
      </div>
    </div>
    <div class="container">
      <ArticleList />
    </div>
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const store = useCounterStore()

onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
.article-page {
  min-height: 100vh;
  background: #f8f9fa;
}

.hero-section {
  background: linear-gradient(135deg, #0066ff, #0044cc);
  padding: 30px 0;
  color: white;
  margin-bottom: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h1 {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}

.create-button {
  background: white;
  color: #0066ff;
  padding: 12px 24px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.create-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .hero-section {
    padding: 40px 0;
  }

  h1 {
    font-size: 24px;
  }

  .create-button {
    padding: 10px 20px;
    font-size: 14px;
  }
}
</style>

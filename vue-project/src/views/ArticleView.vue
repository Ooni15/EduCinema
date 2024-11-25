<template>
  <div class="article-page">
    <div class="header">
      <h1>영화 게시글</h1>
      <RouterLink :to="{ name: 'CreateView' }" class="create-button">
        게시글 작성
      </RouterLink>
    </div>
    <ArticleList />
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
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.create-button {
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.create-button:hover {
  background-color: #3aa876;
}
</style>

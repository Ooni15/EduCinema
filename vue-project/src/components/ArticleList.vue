<template>
  <div class="article-grid">
    <ArticleListItem 
      v-for="article in store.articles"
      :key="article.id"
      :article="article"
    />
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
</script>

<style scoped>
.article-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 5개의 열 */
  gap: 20px;
  padding: 20px;
}

@media (max-width: 1200px) {
  .article-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 992px) {
  .article-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .article-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
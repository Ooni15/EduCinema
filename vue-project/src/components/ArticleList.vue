// ArticleList.vue
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
  grid-template-columns: repeat(3, 1fr); /* 가로 3개 배치 */
  gap: 30px; /* 카드 간격 */
  padding: 40px;
  justify-items: center; /* 중앙 정렬 */
}

@media (max-width: 992px) {
  .article-grid {
    grid-template-columns: repeat(2, 1fr); /* 화면 크기 줄어들면 2개 */
  }
}

@media (max-width: 576px) {
  .article-grid {
    grid-template-columns: repeat(1, 1fr); /* 작은 화면에서는 1개 */
  }
}
</style>

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
  grid-template-columns: repeat(5, 1fr); /* 5 columns by default */
  gap: 20px;
  padding: 20px;
}

@media (max-width: 1200px) {
  .article-grid {
    grid-template-columns: repeat(4, 1fr); /* Adjust to 4 columns */
  }
}

@media (max-width: 992px) {
  .article-grid {
    grid-template-columns: repeat(3, 1fr); /* Adjust to 3 columns */
  }
}

@media (max-width: 768px) {
  .article-grid {
    grid-template-columns: repeat(2, 1fr); /* Adjust to 2 columns */
  }
}

@media (max-width: 576px) {
  .article-grid {
    grid-template-columns: repeat(1, 1fr); /* Single column for smaller screens */
  }
}
</style>
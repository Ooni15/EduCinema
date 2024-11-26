<template>
  <div class="article-page">
    <!-- 네비게이션 경로 -->
    <div class="breadcrumb">
      <div class="container">
        <p>Home > 게시글</p>
      </div>
    </div>

    <!-- 상단 Hero 섹션 -->
    <div class="hero-section">
      <div class="container">
        <div class="header-content">
          <h1>게시글 조회</h1>
        </div>
      </div>
    </div>

    <!-- 게시글 리스트 -->
    <div class="container article-list-container">
      <ArticleList />
    </div>

    <!-- 게시글 작성 버튼 -->
    <div class="container create-button-container">
      <RouterLink :to="{ name: 'CreateView' }" class="create-button">
        게시글 작성하기
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue';
import { onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';

const store = useCounterStore();

onMounted(() => {
  store.getArticles();
});
</script>

<style scoped>
.article-page {
  background: #f9f9f9;
  font-family: Arial, sans-serif;
  padding: 20px 0;
}

.breadcrumb {
  background-color: #f0f0f0;
  padding: 10px 20px;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.breadcrumb p {
  margin: 0;
  color: #333;
  font-size: 14px;
}

.hero-section {
  margin-bottom: 30px;
  text-align: center;
}

.hero-section h1 {
  font-size: 36px;
  font-weight: bold;
  color: #000;
}

.article-list-container {
  margin-bottom: 30px;
}

.create-button-container {
  text-align: center;
}

.create-button {
  display: inline-block;
  padding: 15px 30px;
  font-size: 16px;
  font-weight: bold;
  color: #fff;
  background-color: #000;
  border-radius: 5px;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.create-button:hover {
  background-color: #333;
}
</style>


<template>
  <div class="article-page">
    

    <!-- 상단 Hero 섹션 -->
    <div class="hero-section">
      <div class="container">
        <div class="header-content">
          <h1>영화 기반 학습 자료</h1>
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
/* 전체 페이지 스타일 */
.article-page {
  background: #f9f9f9;
  font-family: Arial, sans-serif;
  padding: 20px 0;
}

/* 네비게이션 경로 스타일 */
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

/* Hero 섹션 */
.hero-section {
  margin-bottom: 30px;
  text-align: center;
}

.hero-section h1 {
  background-color:  #f1f3f5;
  color:   #333;
  text-align: center;
  padding: 40px 20px;
  font-size: 1.8rem;
  margin: 0;
  font-weight: bold;
  color: #000;
}

/* 게시글 리스트 컨테이너 */
.article-list-container {
  margin-bottom: 30px;
}

/* 게시글 작성 버튼 컨테이너 */
.create-button-container {
  text-align: center;
}

/* 게시글 작성 버튼 스타일 */
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

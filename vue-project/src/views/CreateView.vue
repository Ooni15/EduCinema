<template>
  <div class="create-form">
    <h2>새 게시글 작성</h2>
    <form @submit.prevent="createArticle">
      <div class="form-group">
        <input v-model="article.title" type="text" placeholder="제목" required>
      </div>
      
      <div class="form-group">
        <select v-model="article.movie_id" required>
          <option value="" disabled>영화 선택</option>
          <option v-for="movie in movies" :key="movie.id" :value="movie.id">
            {{ movie.movie_title }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <select v-model="article.related_major" required>
          <option value="" disabled>전공 선택</option>
          <option value="전자공학">전자공학</option>
          <!-- 다른 전공 옵션들 추가 -->
        </select>
      </div>

      <div class="form-group">
        <select v-model="article.technology_type" required>
          <option value="" disabled>기술 선택</option>
          <option value="비행 제어">비행 제어</option>
          <!-- 다른 기술 옵션들 추가 -->
        </select>
      </div>

      <div class="form-group">
        <textarea v-model="article.movie_description" placeholder="영화 기술 설명" required></textarea>
      </div>

      <div class="form-group">
        <input v-model="article.short_description" type="text" placeholder="한 줄 소개" required>
      </div>

      <div class="form-group">
        <v-file-input
          v-model="learningMaterial"
          label="학습자료 업로드 (PPT, PDF)"
          accept=".pdf,.ppt,.pptx"
          @change="handleFileUpload"
        ></v-file-input>
      </div>

      <button type="submit">작성완료</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()

const articleData = ref({
  title: '',
  content: '',
  related_major: '',
  technology_type: '',
  movie_description: '',
  short_description: '',
  movie_id: '',
  learning_material: null
})

const handleSubmit = async () => {
  try {
    await store.createArticle(articleData.value)
    router.push({ name: 'ArticleView' })
  } catch (error) {
    console.error('게시글 작성 실패:', error)
  }
}
</script>

<style>

</style>

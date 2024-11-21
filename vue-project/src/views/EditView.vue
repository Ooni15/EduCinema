<template>
    <div class="edit-form">
      <h2>게시글 수정</h2>
      <form @submit.prevent="updateArticle">
        <div class="form-group">
          <label>제목:</label>
          <input v-model="article.title" type="text" required>
        </div>
        
        <div class="form-group">
          <label>내용:</label>
          <textarea v-model="article.content" required></textarea>
        </div>
  
        <div class="form-group">
          <label>관련 전공:</label>
          <select v-model="article.related_major" required>
            <option :value="article.related_major">{{ article.related_major }}</option>
            <option value="전자공학">전자공학</option>
            <option value="기계공학">기계공학</option>
            <option value="컴퓨터공학">컴퓨터공학</option>
            <option value="항공우주공학">항공우주공학</option>
            <option value="물리학">물리학</option>
          </select>
        </div>
  
        <div class="form-group">
          <label>기술 분야:</label>
          <select v-model="article.technology_type" required>
            <option :value="article.technology_type">{{ article.technology_type }}</option>
            <option value="비행 제어">비행 제어</option>
            <option value="로켓 추진">로켓 추진</option>
            <option value="인공위성">인공위성</option>
            <option value="우주 통신">우주 통신</option>
            <option value="우주 환경">우주 환경</option>
          </select>
        </div>
  
        <div class="form-group">
          <label>현재 학습자료:</label>
          <p v-if="article.learning_material_url">{{ article.learning_material_url.split('/').pop() }}</p>
          <p v-else>등록된 파일 없음</p>
          <input
            type="file"
            @change="handleFileUpload"
            accept=".pdf,.ppt,.pptx"
          >
        </div>
  
        <button type="submit">수정완료</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useCounterStore } from '@/stores/counter'
  
  const store = useCounterStore()
  const route = useRoute()
  const router = useRouter()
  const article = ref({})
  const newFile = ref(null)
  
  onMounted(async () => {
    try {
      const response = await store.getArticleDetail(route.params.id)
      article.value = response
    } catch (error) {
      console.error('게시글 로딩 실패:', error)
    }
  })
  
  const handleFileUpload = (event) => {
    newFile.value = event.target.files[0]
  }
  
  const updateArticle = async () => {
  try {
    // 필요한 데이터만 추출하여 전송
    const updateData = {
      title: article.value.title,
      content: article.value.content,
      related_major: article.value.related_major,
      technology_type: article.value.technology_type
    }

    await store.updateArticle(route.params.id, updateData)
    router.push({ 
      name: 'DetailView', 
      params: { id: route.params.id } 
    })
  } catch (error) {
    console.error('게시글 수정 실패:', error)
  }
}
  </script>
  
  <style scoped>
  .edit-form {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  input, textarea, select {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  textarea {
    min-height: 100px;
    resize: vertical;
  }
  
  select {
    background-color: white;
  }
  
  button {
    padding: 8px 16px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #3aa876;
  }
  </style>
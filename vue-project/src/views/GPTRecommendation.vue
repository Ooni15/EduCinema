<template>
    <div class="recommendation-page">
        <div class="container">
            <div class="recommendation-card">
                <h2>AI 맞춤 추천</h2>
                <div v-if="userInfo" class="user-info">
                    <p><strong>전공:</strong> {{ userInfo.major }}</p>
                    <p><strong>사용자:</strong> {{ userInfo.username }}</p>
                    <p>{{ userInfo.major }}전문가 {{ userInfo.username }}님에게 영화에 등장하는 기술을 활용하여 교육 자료나 수업 계획을 작성할 수 있는 아이디어를 추천 받으시겠습니까?</p>
                </div>
    
                <div v-if="recommendations" class="recommendations-list">
                    <h3>추천 교육 자료</h3>
                    <div class="recommendation-content" v-html="formattedRecommendations"></div>
                </div>
    
                <button 
                    @click="getRecommendations" 
                    :disabled="!userInfo || loading" 
                    class="recommend-button"
                >
                    {{ loading ? '추천 중...' : '추천 받기' }}
                </button>
            </div>
        </div>
    </div>
    </template>
    
    <script setup>
    import { ref, onMounted, computed } from 'vue'  // computed 추가
    import { useCounterStore } from '@/stores/counter'
    import axios from 'axios'
    
    const store = useCounterStore()
    const userInfo = ref(null)
    const recommendations = ref(null)
    const loading = ref(false)
    
    // 마크다운 형식 제거 및 HTML 형식으로 변환
    const formattedRecommendations = computed(() => {
      if (!recommendations.value) return ''
      
      return recommendations.value
        .replace(/\*\*/g, '') // ** 제거
        .replace(/###/g, '<h4>') // ### 를 h4 태그로 변환
        .replace(/\n/g, '<br>') // 줄바꿈을 <br>로 변환
        .replace(/- /g, '• ') // 리스트 항목을 불릿으로 변환
    })
    
    onMounted(async () => {
      try {
        const response = await axios.get(`${store.API_URL}/accounts/me/`, {
          headers: {
            Authorization: `Token ${store.token}`
          }
        })
        userInfo.value = response.data
      } catch (error) {
        console.error('사용자 정보 가져오기 실패:', error)
      }
    })
    
    const getRecommendations = async () => {
      if (!userInfo.value?.major) {
        alert('전공 정보가 필요합니다.')
        return
      }
    
      loading.value = true
      try {
        const response = await axios.post(
          `${store.API_URL}/articles/recommendations/`,
          {
            user_major: userInfo.value.major
          },
          {
            headers: {
              Authorization: `Token ${store.token}`
            }
          }
        )
        recommendations.value = response.data.recommendations
      } catch (error) {
        console.error('추천 받기 실패:', error)
        alert('추천을 가져오는데 실패했습니다.')
      } finally {
        loading.value = false
      }
    }
    </script>
  
<style scoped>
.recommendation-page {
padding: 40px 0;
background: #f8f9fa;
min-height: calc(100vh - 60px);
}

.recommendation-card {
background: white;
border-radius: 16px;
padding: 24px;
box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
max-width: 800px;
margin: 0 auto;
}

.user-info {
margin: 20px 0;
padding: 15px;
background: #f8f9fa;
border-radius: 8px;
}

.recommendations-list {
margin: 20px 0;
}

.recommendation-content {
  padding: 20px;
  line-height: 1.6;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.recommendation-content h4 {
  color: #2c3e50;
  margin: 20px 0 10px 0;
  font-size: 1.2em;
}

.recommendation-content br {
  margin-bottom: 8px;
}

.recommend-button {
background: #0066ff;
color: white;
border: none;
padding: 12px 24px;
border-radius: 8px;
cursor: pointer;
font-weight: 600;
width: 100%;
margin-top: 20px;
}

.recommend-button:disabled {
background: #cccccc;
cursor: not-allowed;
}

.loading {
text-align: center;
margin: 20px 0;
color: #666;
}
</style>
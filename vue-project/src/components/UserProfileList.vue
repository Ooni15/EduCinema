<template>
    <div class="profile-page">
    <!-- 상단 제목 -->
    <div class="hero-section">
        <h1>사용자 프로필 리스트</h1>
    </div>

    <!-- 프로필 리스트 -->
    <div class="profile-grid">
        <div 
        v-for="user in users" 
        :key="user.id" 
        class="profile-card"
        >
        <img 
            v-if="user.profile_picture" 
            :src="getProfilePictureUrl(user.profile_picture)" 
            alt="Profile Picture" 
            class="profile-picture"
        />
        <div class="profile-info">
            <h2>{{ user.username }}</h2>
            <p>{{ user.major }}</p>
        </div>
        </div>
    </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '@/stores/user';

const store = useUserStore();
const users = store.users;

const getProfilePictureUrl = (path) => {
    const BASE_URL = 'http://127.0.0.1:8000';
    return `${BASE_URL}${path}`;
};

// 사용자 리스트 가져오기
onMounted(() => {
    store.fetchUsers();
});
</script>

<style scoped>
.profile-page {
    min-height: 100vh;
    background: #f9f9f9; /* 배경색 설정 */
    padding: 20px 0;
    font-family: Arial, sans-serif;
}

.hero-section {
    text-align: center;
    margin-bottom: 30px;
}

.hero-section h1 {
    font-size: 36px;
    font-weight: bold;
    color: #000; /* 검정색 텍스트 */
}

.profile-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* 가로 3개 배치 */
    gap: 30px; /* 카드 간격 */
    padding: 0 20px;
    justify-items: center;
}

@media (max-width: 992px) {
    .profile-grid {
    grid-template-columns: repeat(2, 1fr); /* 화면 크기 줄어들면 2개 */
    }
}

@media (max-width: 576px) {
    .profile-grid {
    grid-template-columns: repeat(1, 1fr); /* 작은 화면에서는 1개 */
    }
}

.profile-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
    width: 100%;
    max-width: 280px;
    text-align: center;
    padding: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-card:hover {
    transform: translateY(-10px); /* 호버 시 부드럽게 올라감 */
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15); /* 호버 그림자 */
}

.profile-picture {
    width: 80px;
    height: 80px;
    border-radius: 50%; /* 동그란 이미지 */
    margin-bottom: 12px;
    object-fit: cover; /* 이미지 비율 유지 */
    background: #f0f0f0; /* 로딩 중 배경 */
}

.profile-info h2 {
    font-size: 18px; /* 이름 크기 */
    font-weight: bold;
    margin: 0;
    color: #000;
}

.profile-info p {
    margin: 8px 0 0;
    font-size: 14px; /* 전공 텍스트 크기 */
    color: #666;
}
</style>

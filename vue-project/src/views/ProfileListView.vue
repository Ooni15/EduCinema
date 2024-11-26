<template>
    <div class="profile-page">
    <!-- 상단 제목 -->
    <div class="hero-section">
        <h1>사용자 프로필 리스트</h1>
    </div>

    <!-- 새로고침 버튼
    <div class="refresh-button-container">
        <button @click="refreshUsers" class="refresh-button">새로고침</button>
    </div> -->

    <!-- 프로필 리스트 -->
    <div class="profile-grid">
        <RouterLink
        v-for="user in users"
        :key="user.id"
        :to="{ name: 'ProfileDetailView', params: { userId: user.id } }"
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
        </RouterLink>
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
const refreshUsers = () => {
    store.fetchUsers();
};

// 컴포넌트가 로드되면 사용자 리스트 가져오기
onMounted(() => {
    refreshUsers();
});
</script>

<style scoped>
/* 전체 페이지 배경 */
.profile-page {
    min-height: 100vh;
    background: #f9f9f9; /* 연한 회색 배경 */
    padding: 20px 0;
    font-family: Arial, sans-serif;
}

/* 제목 스타일 */
.hero-section {
    text-align: center;
    margin-bottom: 30px;
}

.hero-section h1 {
    font-size: 36px;
    font-weight: bold;
    color: #000; /* 검정 텍스트 */
}

/* 새로고침 버튼 */
.refresh-button-container {
    text-align: center;
    margin-bottom: 20px;
}

.refresh-button {
    padding: 12px 24px;
    background: #333; /* 짙은 회색 */
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.refresh-button:hover {
    background-color: #555;
}

/* 프로필 카드 그리드 */
.profile-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* 가로 3개 */
    gap: 30px;
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

/* 프로필 카드 스타일 */
.profile-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
    width: 100%;
    max-width: 280px;
    text-align: center;
    padding: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-decoration: none; /* 링크 스타일 제거 */
    color: inherit; /* 텍스트 색상 상속 */
}

.profile-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15); /* 호버 시 강조 */
}

/* 프로필 사진 */
.profile-picture {
    width: 80px;
    height: 80px;
    border-radius: 50%; /* 동그란 이미지 */
    margin-bottom: 12px;
    object-fit: cover;
    background: #f0f0f0;
}

/* 프로필 정보 */
.profile-info h2 {
    font-size: 18px; /* 이름 크기 */
    font-weight: bold;
    margin: 0;
    color: #000;
}

.profile-info p {
    margin: 8px 0 0;
    font-size: 14px; /* 전공 크기 */
    color: #666;
}
</style>

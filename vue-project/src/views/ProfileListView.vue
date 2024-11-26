<template>
<div>
    <h1>Profiles</h1>
    <button @click="refreshUsers">새로고침</button>
    <ul>
    <li v-for="user in users" :key="user.id">
        <RouterLink :to="{ name: 'ProfileDetailView', params: { userId: user.id } }">
        {{ user.username }} - {{ user.major }}
        </RouterLink>
        <img 
        v-if="user.profile_picture" 
        :src="getProfilePictureUrl(user.profile_picture)" 
        alt="Profile Picture" 
        width="100"
        />
    </li>
    </ul>
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

<template>
<div>
    <h1>사용자 프로필 리스트</h1>
    <ul>
    <li v-for="user in users" :key="user.id">
        <router-link :to="{ name: 'ProfileDetailView', params: { userId: user.id }}">
        {{ user.username }}
        </router-link>
    </li>
    </ul>
</div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '@/stores/user';

const store = useUserStore();

// 사용자 리스트 가져오기
onMounted(() => {
store.fetchUsers();
});

const users = store.users;
</script>

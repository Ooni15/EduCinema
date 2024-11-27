<template>
    <div>
        <h1>{{ user?.username }}님의 프로필</h1>
        <p><strong>이메일:</strong> {{ user?.email }}</p>
        <p><strong>전공:</strong> {{ user?.major }}</p>
        <p><strong>자기소개:</strong> {{ user?.bio }}</p>
        <img v-if="user?.profile_picture" :src="`http://127.0.0.1:8000${user.profile_picture}`" alt="프로필 사진" />
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRoute } from 'vue-router';

const store = useUserStore();
const route = useRoute();
const userId = route.params.userId;

// 특정 사용자 상세 정보 가져오기
onMounted(() => {
store.fetchUserDetail(userId);
});

const user = store.userDetail;
</script>

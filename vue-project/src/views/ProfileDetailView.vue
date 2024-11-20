<template>
<div v-if="userDetail">
    <h1>{{ userDetail.username }}'s Profile</h1>
    <p><strong>Major:</strong> {{ userDetail.major }}</p>
    <p><strong>Bio:</strong> {{ userDetail.bio }}</p>
    <img v-if="userDetail.profile_picture" :src="userDetail.profile_picture" alt="Profile Picture" />
</div>
<div v-else>
    <p>Loading profile...</p>
</div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { onMounted } from 'vue';
import { useUserStore } from '@/stores/user';

const route = useRoute();
const store = useUserStore();
const userDetail = store.userDetail;

// 특정 사용자 프로필 가져오기
onMounted(() => {
const userId = route.params.userId;
store.fetchUserDetail(userId);
});
</script>

<style scoped>
img {
max-width: 200px;
border-radius: 10px;
}
</style>

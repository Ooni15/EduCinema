<template>
<div>
    <h1>Profiles</h1>
    <ul>
    <li v-for="user in users" :key="user.id">
        <!-- 사용자 이름과 전공 표시, 클릭하면 상세 페이지로 이동 -->
        <RouterLink :to="{ name: 'ProfileDetailView', params: { userId: user.id } }">
        {{ user.username }} - {{ user.major }}
        </RouterLink>
    </li>
    </ul>
</div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '@/stores/user'; // Pinia의 User 스토어 사용

const store = useUserStore();
const users = store.users;

// 컴포넌트가 로드되면 사용자 리스트 가져오기
onMounted(() => {
store.fetchUsers();
});
</script>

<style scoped>
ul {
list-style: none;
padding: 0;
}
li {
margin: 10px 0;
}
</style>

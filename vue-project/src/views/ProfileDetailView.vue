<template>
<div>
    <h1>{{ user?.username }}님의 프로필</h1>
    <p><strong>이메일:</strong> {{ user?.email }}</p>
    <p><strong>전공:</strong> {{ user?.major }}</p>
    <p><strong>자기소개:</strong> {{ user?.bio }}</p>
    <img v-if="user?.profile_picture" :src="`http://127.0.0.1:8000${user.profile_picture}`" alt="프로필 사진" />

    <!-- 댓글 섹션 -->
    <div>
    <h2>댓글</h2>
    <ul>
        <li v-for="comment in comments" :key="comment.id">
        <p><strong>{{ comment.username }}</strong>: {{ comment.content }}</p>
        <small>{{ comment.created_at }}</small>
        <!-- 수정 및 삭제 버튼 -->
        <button @click="editComment(comment.id, '수정된 내용')">수정</button>
        <button @click="deleteComment(comment.id)">삭제</button>
        </li>
    </ul>

    <!-- 댓글 추가 -->
    <form @submit.prevent="submitComment">
        <textarea v-model="newComment" placeholder="댓글을 입력하세요"></textarea>
        <button type="submit">댓글 작성</button>
    </form>
    </div>
</div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useProfileCommentsStore } from '@/stores/profileComments';

const userStore = useUserStore();
const commentsStore = useProfileCommentsStore();

const route = useRoute();
const userId = route.params.userId;

const user = userStore.userDetail;
const comments = commentsStore.comments;
const newComment = ref('');

// 사용자 프로필 정보 및 댓글 가져오기
onMounted(() => {
userStore.fetchUserDetail(userId);
commentsStore.fetchComments(userId); // 수정됨
});

// 댓글 추가
const submitComment = () => {
if (newComment.value.trim()) {
    commentsStore.addComment(userId, newComment.value.trim());
    newComment.value = ''; // 입력창 초기화
} else {
    alert('댓글 내용을 입력하세요.');
}
};

// 댓글 수정
const editComment = (commentId, content) => {
commentsStore.editComment(commentId, content);
};

// 댓글 삭제
const deleteComment = (commentId) => {
commentsStore.deleteComment(commentId);
};
</script>

<style scoped>
/* 필요한 스타일 추가 */
</style>

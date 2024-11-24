<template>
<div>
    <h1>{{ user?.username }}님의 프로필</h1>
    <p><strong>이메일:</strong> {{ user?.email }}</p>
    <p><strong>전공:</strong> {{ user?.major }}</p>
    <p><strong>자기소개:</strong> {{ user?.bio }}</p>
    <img
    v-if="user?.profile_picture"
    :src="`http://127.0.0.1:8000${user.profile_picture}`"
    alt="프로필 사진"
    width="150"
    />

    <hr />

    <!-- 댓글 섹션 -->
    <div>
    <h2>댓글</h2>
    <ul>
        <li v-for="comment in comments" :key="comment.id">
        <p>
            <strong>{{ comment.username }}</strong>: {{ comment.content }}
        </p>
        <small>{{ comment.created_at }}</small>

        <!-- 수정 및 삭제 버튼 -->
        <button
            v-if="comment.username === currentUser"
            @click="toggleEdit(comment.id)"
        >
            수정
        </button>
        <button
            v-if="comment.username === currentUser"
            @click="deleteComment(comment.id)"
        >
            삭제
        </button>

        <!-- 수정 폼 -->
        <div v-if="editingCommentId === comment.id">
            <textarea v-model="newContent"></textarea>
            <button @click="editComment(comment.id, newContent)">수정 완료</button>
            <button @click="cancelEdit">취소</button>
        </div>
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
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useProfileCommentsStore } from '@/stores/profileComments';

const userStore = useUserStore();
const commentsStore = useProfileCommentsStore();

const route = useRoute();
const userId = ref(route.params.userId);

const user = ref(null);
const comments = ref([]);
const loading = ref(true);

const newComment = ref('');
const newContent = ref('');
const editingCommentId = ref(null);
const currentUser = ref(localStorage.getItem('username')); // 현재 로그인 사용자
console.log('현재 사용자:', currentUser.value);
// localStorage가 변경되면 currentUser를 업데이트
watch(
    () => localStorage.getItem('username'),
    (newUsername) => {
        currentUser.value = newUsername;
        console.log('currentUser 업데이트됨:', currentUser.value);
    }
);

// 사용자 프로필 정보 및 댓글 정보 가져오기
const fetchData = async () => {
loading.value = true;
user.value = null;
comments.value = [];
await userStore.fetchUserDetail(userId.value);
await commentsStore.fetchComments(userId.value);
user.value = userStore.userDetail;
comments.value = commentsStore.comments;
loading.value = false;
};

// 라우트 변경 시 데이터 다시 가져오기
watch(
() => route.params.userId,
(newId) => {
    userId.value = newId;
    fetchData();
}
);

// 처음 마운트될 때 데이터 가져오기
onMounted(fetchData);

// 댓글 추가
const submitComment = () => {
if (newComment.value.trim()) {
    commentsStore.addComment(userId.value, newComment.value.trim());
    newComment.value = '';
} else {
    alert('댓글 내용을 입력하세요.');
}
};

// 댓글 수정
const toggleEdit = (commentId) => {
    editingCommentId.value = commentId;
    const comment = comments.value.find((comment) => comment.id === commentId);
    newContent.value = comment ? comment.content : '';
    console.log('현재 사용자:', currentUser.value);
};

const editComment = async (commentId, content) => {
    if (!content.trim()) {
        alert('수정할 내용을 입력하세요.');
        return;
    }
    try {
        // 댓글 수정 요청
        await commentsStore.editComment(commentId, content.trim());

        // 수정 모드 종료
        editingCommentId.value = null;
        newContent.value = '';

        // 수정된 댓글 데이터 가져오기
        const updatedCommentIndex = comments.value.findIndex(
        (comment) => comment.id === commentId
        );
        if (updatedCommentIndex !== -1) {
        comments.value[updatedCommentIndex].content = content.trim();
        }
    } catch (err) {
        console.error('댓글 수정 실패:', err.response?.data || err);
        alert('댓글 수정 중 오류가 발생했습니다.');
    }
    };


const cancelEdit = () => {
editingCommentId.value = null;
newContent.value = '';
};

// 댓글 삭제
const deleteComment = async (commentId) => {
try {
    await commentsStore.deleteComment(commentId);
    fetchData(); // 데이터 다시 가져오기
} catch (err) {
    console.error('댓글 삭제 실패:', err.response?.data || err);
    alert('댓글 삭제 중 오류가 발생했습니다.');
}
};
</script>

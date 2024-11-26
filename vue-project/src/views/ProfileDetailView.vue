<template>
    <div class="profile-page">
        <!-- 프로필 섹션 -->
        <div class="profile-section">
            <img
                v-if="user?.profile_picture"
                :src="`http://127.0.0.1:8000${user.profile_picture}`"
                alt="프로필 사진"
                class="profile-picture"
            />
            <div class="profile-info">
                <h1>{{ user?.username }}</h1>
                <p><strong>이메일:</strong> {{ user?.email }}</p>
                <p><strong>전공:</strong> {{ user?.major }}</p>
                <p><strong>자기소개:</strong> {{ user?.bio }}</p>
            </div>
        </div>
    
        <hr class="divider" />
    
        <!-- 게시글 섹션 -->
        <div class="articles-section">
            <h2>게시글 목록</h2>
            <ul class="article-list">
                <li v-for="(article, index) in articles" :key="article.id" class="article-card">
                    <h3>
                        {{ index + 1 }}.
                        <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }" class="article-link">
                            {{ article.title }}
                        </RouterLink>
                    </h3>
                    <p class="article-content">{{ article.content }}</p>
                    <small>작성일: {{ formatDate(article.created_at) }}</small>
                </li>
            </ul>
        </div>
    
        <hr class="divider" />
    
        <!-- 댓글 섹션 -->
        <div class="comments-section">
            <h2>댓글</h2>
            <ul class="comments-list">
                <li v-for="comment in comments" :key="comment.id" class="comment-card">
                    <p><strong>{{ comment.username }}</strong>: {{ comment.content }}</p>
                    <small>{{ formatDate(comment.created_at) }}</small>
    
                    <!-- 수정 및 삭제 버튼 -->
                    <div v-if="comment.username === currentUser" class="comment-actions">
                        <button @click="toggleEdit(comment.id)">수정</button>
                        <button @click="deleteComment(comment.id)">삭제</button>
                    </div>
    
                    <!-- 수정 폼 -->
                    <div v-if="editingCommentId === comment.id" class="edit-comment-form">
                        <textarea v-model="newContent" class="edit-textarea"></textarea>
                        <button @click="editComment(comment.id, newContent)" class="submit-edit-button">수정 완료</button>
                        <button @click="cancelEdit" class="cancel-edit-button">취소</button>
                    </div>
                </li>
            </ul>
    
            <!-- 댓글 추가 -->
            <form @submit.prevent="submitComment" class="add-comment-form">
                <textarea v-model="newComment" placeholder="댓글을 입력하세요" class="comment-textarea"></textarea>
                <button type="submit" class="submit-comment-button">댓글 작성</button>
            </form>
        </div>
    </div>
</template>


<script setup>
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useProfileCommentsStore } from '@/stores/profileComments';
import { useCounterStore } from '@/stores/counter';

const userStore = useUserStore();
const commentsStore = useProfileCommentsStore();
const counterStore = useCounterStore();

const route = useRoute();
const userId = ref(route.params.userId);

const user = ref(null);
const articles = ref([]);
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
articles.value = [];
await userStore.fetchUserDetail(userId.value);
await commentsStore.fetchComments(userId.value);
const userArticles = await counterStore.getArticlesByUser(userId.value);
user.value = userStore.userDetail;
comments.value = commentsStore.comments;
articles.value = userArticles;
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

// 날짜 포맷팅 함수
const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('ko-KR');
};
</script>

<style scoped>
/* 전체 페이지 스타일 */
.profile-page {
  background: #f9f9f9;
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* 프로필 섹션 */
.profile-section {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
  padding: 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.profile-picture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-info h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
}

.profile-info p {
  margin: 4px 0;
}

.profile-info strong {
  font-weight: bold;
}

/* hr 스타일 */
.divider {
  border: 0;
  border-top: 1px solid #ddd;
  margin: 20px 0;
}

/* 게시글 섹션 */
.articles-section {
  margin: 20px 0;
}

.article-list {
  list-style: none;
  padding: 0;
}

.article-card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.article-link {
  text-decoration: none;
  color: #0066ff;
}

.article-link:hover {
  text-decoration: underline;
}

.article-content {
  margin: 8px 0;
  color: #555;
}

/* 댓글 섹션 */
.comments-section {
  margin: 20px 0;
}

.comments-list {
  list-style: none;
  padding: 0;
}

.comment-card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

/* 댓글 수정 및 삭제 버튼 */
.comment-actions button {
  margin-right: 8px;
  background: #ddd; /* 회색으로 변경 */
  color: black;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
}

.comment-actions button:hover {
  background: #bbb;
}

.edit-comment-form {
  margin-top: 12px;
}

.edit-textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 8px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.submit-edit-button,
.cancel-edit-button {
  margin-right: 8px;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.submit-edit-button {
  background: #ddd;
  color: black;
}

.submit-edit-button:hover {
  background: #bbb;
}

.cancel-edit-button {
  background: #ddd;
  color: black;
}

.cancel-edit-button:hover {
  background: #bbb;
}

/* 댓글 작성 박스 */
.comment-textarea {
  width: 100%;
  padding: 12px;
  margin-bottom: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

.submit-comment-button {
  padding: 12px 24px;
  background: #333;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.submit-comment-button:hover {
  background: #555;
}
</style>


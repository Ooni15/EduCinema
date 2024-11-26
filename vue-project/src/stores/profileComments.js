import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useProfileCommentsStore = defineStore('profileComments', () => {
const API_URL = 'http://127.0.0.1:8000/api/v1/accounts/'; // Django API URL
const comments = ref([]); // 특정 프로필의 댓글 리스트

// 로컬 스토리지에서 토큰을 안전하게 가져오기
const getToken = () => {
const token = localStorage.getItem('token');
if (!token) {
    console.error('토큰이 존재하지 않습니다. 로그인이 필요합니다.');
}
return token;
};

// 특정 사용자의 댓글 가져오기
const fetchComments = async (userId) => {
const token = getToken();
if (!token) return;

try {
    const res = await axios.get(`${API_URL}users/${userId}/comments/`, {
    headers: {
        Authorization: `Token ${token}`,
    },
    });
    comments.value = res.data; // 댓글 리스트 저장
} catch (err) {
    console.error('댓글 가져오기 실패:', err.response?.data || err);
}
};

// 댓글 추가하기
const addComment = async (userId, content) => {
const token = getToken();
if (!token) return;

try {
    const res = await axios.post(
    `${API_URL}users/${userId}/comments/`,
    { content },
    {
        headers: {
        Authorization: `Token ${token}`,
        },
    }
    );
    comments.value.push(res.data); // 새로운 댓글 추가
} catch (err) {
    console.error('댓글 추가 실패:', err.response?.data || err);
}
};

// 댓글 수정하기
const editComment = async (commentId, newContent) => {
const token = getToken();
if (!token) return;

try {
    const res = await axios.put(
    `${API_URL}comments/${commentId}/`,
    { content: newContent },
    {
        headers: {
        Authorization: `Token ${token}`,
        },
    }
    );
    const index = comments.value.findIndex((comment) => comment.id === commentId);
    if (index !== -1) {
    comments.value[index] = res.data; // 수정된 댓글 반영
    }
} catch (err) {
    console.error('댓글 수정 실패:', err.response?.data || err);
}
};

// 댓글 삭제하기
const deleteComment = async (commentId) => {
const token = getToken();
if (!token) return;

try {
    await axios.delete(`${API_URL}comments/${commentId}/`, {
    headers: {
        Authorization: `Token ${token}`,
    },
    });
    comments.value = comments.value.filter((comment) => comment.id !== commentId); // 삭제된 댓글 제거
} catch (err) {
    console.error('댓글 삭제 실패:', err.response?.data || err);
}
};

return {
comments,
fetchComments,
addComment,
editComment,
deleteComment,
};
});

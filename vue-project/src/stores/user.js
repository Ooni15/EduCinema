import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('user', () => {
    const API_URL = 'http://127.0.0.1:8000/api/v1/accounts/';
    const users = ref([]); // 사용자 리스트
    const userDetail = ref(null); // 상세 사용자 정보
    const token = ref(null); // 인증 토큰

  // 사용자 리스트 가져오기
    const fetchUsers = async () => {
    const tokenFromStorage = localStorage.getItem('token'); // 로컬 스토리지에서 토큰 가져오기
    if (!tokenFromStorage) {
        console.error('토큰이 존재하지 않습니다.');
        return;
    }

    try {
        const res = await axios.get(`${API_URL}users/`, {
            headers: {
            Authorization: `Token ${tokenFromStorage}`, // 로컬 스토리지에서 가져온 토큰 사용
        },
    });
    users.value = res.data;
    } catch (err) {
        console.error('사용자 리스트 가져오기 실패:', err.response?.data || err);
    }
    };

  // 특정 사용자 상세 정보 가져오기
    const fetchUserDetail = async (userId) => {
        const tokenFromStorage = localStorage.getItem('token');
        if (!tokenFromStorage) {
            console.error('토큰이 존재하지 않습니다.');
            return;
    }

    try {
        const res = await axios.get(`${API_URL}users/${userId}/`, {
            headers: {
            Authorization: `Token ${tokenFromStorage}`,
            },
        });
        userDetail.value = res.data;
        console.log('사용자 상세 정보:', res.data);
    } catch (err) {
        console.error('사용자 상세 정보 가져오기 실패:', err.response?.data || err);
    }
    };

    return { users, userDetail, fetchUsers, fetchUserDetail, token };
});

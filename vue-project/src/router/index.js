import { createRouter, createWebHistory } from 'vue-router'
import ArticleView from '@/views/ArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import EditView from '@/views/EditView.vue'  // EditView import
import { useCounterStore } from '@/stores/counter'
import ProfileListView from '@/views/ProfileListView.vue';
import ProfileDetailView from '@/views/ProfileDetailView.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'ArticleView',
      component: ArticleView
    },
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView
    },
    {
      path: '/create',
      name: 'CreateView',
      component: CreateView
    },
    {
      path: '/articles/:id/edit',  // 수정 페이지 라우트 추가
      name: 'EditArticle',
      component: EditView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/profiles',
      name: 'ProfileListView',
      component: ProfileListView,
    },
    {
      path: '/profiles/:userId',
      name: 'ProfileDetailView',
      component: ProfileDetailView,
      props: true,
    },
  ]
})

router.beforeEach((to, from) => {
  const store = useCounterStore()
  // 만약 이동하는 목적지가 메인 페이지이면서
  // 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
  if (to.name === 'ArticleView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

  // 만약 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면
  // 메인 페이지로 보냄
  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin)) {
    window.alert('이미 로그인 되어있습니다.')
    return { name: 'ArticleView' }
  }

  // 3. 프로필 관련 페이지 접근 제한
  if ((to.name === 'ProfileListView' || to.name === 'ProfileDetailView') && !store.isLogin) {
    window.alert('로그인이 필요합니다.');
    return { name: 'LogInView' };
  }
})

export default router

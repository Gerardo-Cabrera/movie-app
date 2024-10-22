import { createRouter, createWebHistory } from 'vue-router';
import MovieSearch from '../components/MovieSearch.vue';
import MovieDetail from '../components/MovieDetail.vue';
import ReviewForm from '../components/ReviewForm.vue';
import LoginForm from '@/components/LoginForm.vue';
import FavoriteList from '../components/FavoriteList.vue';
import RegisterForm from '@/components/RegisterForm.vue';

const routes = [
  {
    path: '/',
    name: 'MovieSearch',
    component: MovieSearch
  },
  {
    path: '/movie/:movie_id/:slug?',
    name: 'MovieDetail',
    component: MovieDetail,
    props: route => ({ 
      movie_id: route.params.movie_id, 
      slug: route.params.slug 
    })
  },
  {
    path: '/login',
    name: 'LoginForm',
    component: LoginForm
  },
  {
    path: '/register',
    name: 'RegisterForm',
    component: RegisterForm
  },
  {
    path: '/review/:imdbID',
    name: 'ReviewForm',
    component: ReviewForm,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'FavoriteList',
    component: FavoriteList,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('token');
    if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
      next({ name: 'LoginForm' });
    } else {
      next();
    }
});

export default router;

import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';
import MangaDetail from '../components/MangaDetail.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: MainPage,
  },
  {
    path: '/manga/:mangaId',
    name: 'mangaDetail',
    component: MangaDetail,
    // props: true,
  },
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});

export default router;

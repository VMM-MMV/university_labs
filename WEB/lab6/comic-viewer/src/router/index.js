import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';
import MangaDetail from '../components/MangaDetail.vue';
import Chapter from '../components/Chapter.vue';

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
  },
  {
    path: '/manga/:mangaId/chapter/:chapterName',
    name: 'chapter',
    component: Chapter,
  },
];


const router = createRouter({
  history: createWebHistory("/"),
  routes,
});

export default router;

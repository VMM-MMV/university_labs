import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../views/MainPage.vue';
import MangaDetail from '../views/MangaDetail.vue';
import Chapter from '../views/Chapter.vue';
import Login from '../views/Login.vue';
import Favorites from '../views/Favorites.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: MainPage,
  },
  { path: '/login', name: 'login', component: Login },

  {
    path: '/manga/:mangaId',
    name: 'mangaDetail',
    component: MangaDetail,
  },
  {
    path: '/manga/:mangaId/chapter/:chapterID',
    name: 'chapter',
    component: Chapter,
  },
  {
    path: '/favorites',
    name: 'favorites',
    component: Favorites,
  },
];


const router = createRouter({
  history: createWebHistory("/"),
  routes,
});

export default router;

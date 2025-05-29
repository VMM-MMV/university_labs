<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl text-secondary font-bold mb-6">My Favorites</h1>

    <!-- Empty state using component -->
    <EmptyState 
      v-if="favoriteMangaList.length === 0"
      message="You haven't added any manga to your favorites yet"
    >
      <template #action>
        <router-link to="/" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
          Browse Manga
        </router-link>
      </template>
    </EmptyState>

    <!-- Manga Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
      <MangaCard 
        v-for="manga in favoriteMangaList"
        :key="manga.title"
        :manga="manga"
        :mangaId="manga.mangaID"
        :chapterId="manga.chapterID"
        :imageSrc="manga.img"
        :truncatedDescription="truncateDescription(manga.description)"
        :isFavorite="true"
        :allowGenreFilter="false"
        @toggleFavorite="removeFromFavorites(manga)"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useFavorites } from '../composables/useFavorites';
import MangaCard from '../components/MangaCard.vue';
import EmptyState from '../components/EmptyState.vue';
import { useRestStore } from '../composables/useRestStore';
import { useFormatters } from '../composables/useFormatters';

const { favorites, removeFromFavorites, loadFavorites } = useFavorites();
const { mangaList, loadMangaList } = useRestStore();
const { truncateDescription } = useFormatters();

// Only show manga objects that are in favorites
const favoriteMangaList = computed(() => {
  return mangaList.value.filter(manga => {
    return favorites.value.includes(manga.mangaID);
  });
});

// Ensure everything is loaded on mount
onMounted(() => {
  loadFavorites();
  loadMangaList();
});
</script>

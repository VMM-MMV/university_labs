<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="manga" class="border-2 border-gray-300 rounded-lg shadow-xl bg-white p-6">
      <!-- Image -->
      <div class="h-64 w-full" style="min-height: 250px;">
        <img
          :src="getImageSrc(manga.img_path)"
          alt="Manga cover"
          class="w-full h-full object-cover"
        />
      </div>

      <!-- Manga Title -->
      <h1 class="text-3xl font-bold mt-6">{{ manga.title }}</h1>

      <!-- Manga Description -->
      <p class="text-sm text-gray-600 mt-4">{{ manga.description }}</p>

      <!-- Genres -->
      <div class="flex flex-wrap gap-2 mt-4">
        <template v-for="(genre, index) in manga.genres" :key="index">
          <span class="px-2 py-1 text-xs bg-gray-200 rounded">{{ genre }}</span>
        </template>
      </div>
    </div>
    <div v-else class="text-center text-gray-500 mt-6">Loading manga details...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const manga = ref(null);
const route = useRoute();
const mangaId = route.params.mangaId;

const getImageSrc = (imgPath) => {
  return imgPath || '/api/placeholder/400/640';
};

onMounted(async () => {
  try {
    const response = await fetch(`/manga_store/contents/${mangaId}/info.json`);
    if (response.ok) {
      manga.value = await response.json();
    } else {
      console.error('Failed to load manga details:', response.statusText);
    }
  } catch (error) {
    console.error('Error loading manga details:', error);
  }
});
</script>

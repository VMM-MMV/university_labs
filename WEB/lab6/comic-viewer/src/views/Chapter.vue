<template>
  <div class="container mx-auto px-4 py-8 max-w-3xl">
    <div v-if="images.length > 0" class="bg-white shadow rounded-lg p-6">
      <h1 class="text-2xl font-bold"> {{ chapterName }}</h1>
      <div>
        <img v-for="(img, index) in images" :key="index" :src="img" alt="Chapter page" class="w-full rounded shadow" />
      </div>
    </div>
    <div v-else class="text-center text-gray-500">Loading chapter images...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useMangaStore } from '../composables/useMangaStore';

const route = useRoute();
const mangaId = route.params.mangaId;
const chapterName = route.params.chapterName;

const images = ref([]);

const { loadChapterImages } = useMangaStore();

onMounted(() => {
  loadChapterImages(mangaId, chapterName, (imagePath) => {
    images.value.push(imagePath);
  });
});
</script>

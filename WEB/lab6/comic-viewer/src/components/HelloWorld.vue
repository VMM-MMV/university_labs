<template>
  <div class="container mx-auto px-4 py-8">
    <header class="mb-8">
      <h1 class="text-4xl font-bold text-gray-800 text-center">Manga Library</h1>
    </header>

    <main>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="manga in mangaList"
          :key="manga.title"
          class="bg-white rounded-lg shadow-lg overflow-hidden"
        >
          <div class="h-64 overflow-hidden bg-gray-200">
            <img
              :src="getImageSrc(manga.img_path)"
              alt="Cover image"
              class="w-full h-full object-cover"
            />
          </div>

          <div class="p-6">
            <h2 class="text-xl font-bold text-gray-800 mb-2">{{ manga.title }}</h2>

            <div class="flex items-center mb-4">
              <div class="mr-4">
                <span class="text-sm font-medium text-gray-500">Latest Chapter:</span>
                <span class="text-sm text-gray-700">{{ getChapterName(manga.latestChapter) }}</span>
              </div>
              <div>
                <span class="text-sm font-medium text-gray-500">Views:</span>
                <span class="text-sm text-gray-700">{{ manga.views }}</span>
              </div>
            </div>

            <p class="text-gray-600 mb-4 h-24 overflow-y-auto text-sm">
              {{ truncateDescription(manga.description) }}
            </p>

            <div class="flex justify-end">
              <span
                class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
              >Manga</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const mangaList = ref([]);

const getChapterName = (chapterPath) => {
  const parts = chapterPath.split('\\');
  return parts[parts.length - 1];
};

const getImageSrc = (imgPath) => {
  return imgPath || '/api/placeholder/400/640';
};

const truncateDescription = (desc) => {
  const cleanDesc = desc.replace(/You are reading.*?bookmark\.\n\n\s+/s, '');
  if (cleanDesc.length > 200) {
    return cleanDesc.substring(0, 200) + '...';
  }
  return cleanDesc;
};

onMounted(async () => {
  try {
    console.log("Aaaaa");
    const response = await fetch('/manga_store/store.json');
    if (response.ok) {
      mangaList.value = await response.json();
    } else {
      console.error('Failed to load manga list:', response.statusText);
    }
  } catch (error) {
    console.error('Error loading manga list:', error);
  }
});
</script>

<style>
</style>

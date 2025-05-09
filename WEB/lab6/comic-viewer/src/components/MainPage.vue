<template>
  <div class="container mx-auto px-4 py-8">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
      <div
        v-for="manga in mangaList"
        :key="manga.title"
        class="border-2 border-gray-300 rounded-lg shadow-xl bg-white overflow-hidden flex flex-col mb-8"
        style="box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);"
      >
        <!-- Image -->
        <div class="h-64 w-full" style="min-height: 250px;">
          <img
            :src="getImageSrc(manga.img_path)"
            alt="Manga cover"
            class="w-full h-full object-cover"
          />
        </div>

        <!-- Text content -->
        <div class="p-6 bg-white flex-1 flex flex-col justify-between">
          <div>
            <!-- Title -->
            <h2 class="text-xl font-bold mb-3 min-h-[48px] line-clamp-2">
              {{ manga.title }}
            </h2>
            
            <!-- Chapter and views -->
            <div class="flex items-center justify-center mb-3 min-h-[32px]">
              <div class="mr-4">
                <span class="text-sm font-medium text-gray-500">Latest Chapter:</span>
                <span class="text-sm">{{ getChapterName(manga.latestChapter) }}</span>
              </div>
              <div>
                <span class="text-sm font-medium text-gray-500">Views:</span>
                <span class="text-sm">{{ manga.views }}</span>
              </div>
            </div>

            <!-- Description -->
            <p class="text-sm text-gray-600 mb-3 min-h-[60px] line-clamp-3">
              {{ truncateDescription(manga.description) }}
            </p>

            <!-- Genres container -->
            <div class="flex flex-wrap gap-2 mb-3 flex-grow-0" ref="genresContainer">
              <template v-for="(genre, index) in manga.genres" :key="index">
                <span class="px-2 py-1 text-xs bg-gray-200 rounded">{{ genre }}</span>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
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
    const response = await fetch('/manga_store/store.json');
    if (response.ok) {
      mangaList.value = await response.json();
      console.log(mangaList); 
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
<!-- MangaDetail.vue -->
<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <div v-if="manga" class="border-2 border-gray-300 rounded-lg shadow-lg bg-white overflow-hidden">
      <!-- Top section: Image left, details right -->
      <div class="flex flex-col md:flex-row p-4">
        <!-- Left: Image -->
        <div class="md:w-1/3 mb-4 md:mb-0 md:pr-4">
          <div class="w-full h-64">
            <img
              :src="getImageSrc(manga.img_path)"
              alt="Manga cover"
              class="w-full h-full object-cover rounded-lg"
            />
          </div>
        </div>

        <!-- Right: Details -->
        <div class="md:w-2/3 text-left">
          <h1 class="text-3xl font-bold">{{ manga.title }}</h1>
          <p class="text-sm text-gray-600 mt-2">Author(s): {{ manga.authors.join(', ') }}</p>
          <p class="text-sm text-gray-600 mt-2">{{ manga.lastUpdate }}</p>
          <p class="text-sm text-gray-600 mt-2">Rating: {{ manga.rating.score }} / {{ manga.rating.outOf }} ({{ manga.rating.votes }} votes)</p>
          
          <div class="mt-4 flex flex-wrap gap-2 justify-begin">
            <span
              v-for="(genre, index) in manga.genres"
              :key="index"
              class="px-2 py-1 text-xs bg-gray-200 rounded-full"
            >
              {{ genre }}
            </span>
          </div>
        </div>
      </div>

      <div class="p-4">
        <p class="text-sm text-gray-700">{{ manga.summary }}</p>
      </div>

      <div class="border-t-2 border-gray-200 p-4">
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold">Chapters</h2>
          <button 
            @click="showAllChapters = !showAllChapters" 
            class="text-sm text-blue-600 hover:underline"
          >
            {{ showAllChapters ? 'Show Less' : 'Show All' }}
          </button>
        </div>

        <ul class="mt-3 border rounded-lg">
          <li v-for="(chapter, index) in displayedChapters" :key="index" 
              class="flex justify-between items-center p-3 hover:bg-gray-50"
              :class="{'bg-gray-100': index % 2 === 0}">
                <router-link
                    :to="{
                        name: 'chapter',
                        params: { mangaID: getMangaID(chapter.chapterID), chapterName: chapter.chapterName }
                    }"
                    class="text-sm font-medium text-blue-600 hover:underline"
                    >
                    {{ chapter.chapterName }}
                </router-link>     
                <span class="text-xs text-gray-500">{{ chapter.timeUploaded }} | {{ chapter.views }} views</span>
          </li>
        </ul>

        <div v-if="!showAllChapters && manga.chapters.length > 5" class="text-center mt-2">
          <button 
            @click="showAllChapters = true"
            class="w-full py-2 bg-gray-100 hover:bg-gray-200 rounded-md text-sm"
          >
            Show {{ manga.chapters.length - 5 }} More Chapters
          </button>
        </div>
      </div>
    </div>
    <div v-else class="text-center text-gray-500 mt-6">Loading manga details...</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useMangaStore } from '../composables/useMangaStore';
import { useFormatters } from '../composables/useFormatters';

const route = useRoute();
const mangaId = route.params.mangaId;
const manga = ref(null);
const showAllChapters = ref(false);

const { loadMangaDetails } = useMangaStore();
const { getMangaID, getImageSrc } = useFormatters();

const displayedChapters = computed(() => {
  if (!manga.value) return [];
  return showAllChapters.value ? manga.value.chapters : manga.value.chapters.slice(0, 5);
});

onMounted(async () => {
  try {
    manga.value = await loadMangaDetails(mangaId);
  } catch (error) {
    console.error('Error loading manga details:', error);
  }
});
</script>
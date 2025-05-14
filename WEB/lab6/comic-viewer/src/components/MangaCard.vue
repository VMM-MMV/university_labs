<template>
  <div
    class="border-2 border-gray-300 rounded-lg shadow-xl bg-base-300 overflow-hidden flex flex-col mb-8"
    style="box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);"
  >
    <div class="relative">
      <!-- Favorite Button -->
      <FavoriteButton
        :is-favorite="isFavorite"
        @toggle="$emit('toggleFavorite')"
      />

      <router-link :to="{ name: 'mangaDetail', params: { mangaId: manga.mangaID } }">
        <!-- Image -->
        <div class="h-64 w-full" style="min-height: 250px;">
          <img
            :src="manga.img"
            alt="Manga cover"
            class="w-full h-full object-cover"
          />
        </div>

        <!-- Text content -->
        <div class="p-6 flex-1 flex flex-col justify-between">
          <div>
            <!-- Title -->
            <h2 class="text-primary text-xl font-bold mb-3 min-h-[48px] line-clamp-2">
              {{ manga.title }}
            </h2>

            <!-- Chapter and views -->
            <div class="flex items-center justify-center mb-3 min-h-[32px]">
              <div class="mr-4">
                <span class="text-sm font-medium text-secondary">Latest Chapter:</span>
                <span class="text-sm text-primary">{{ chapterId }}</span>
              </div>
              <div>
                <span class="text-sm font-medium text-secondary">Views:</span>
                <span class="text-sm text-primary">{{ manga.view }}</span>
              </div>
            </div>

            <!-- Description -->
            <p class="text-sm text-accent mb-3 min-h-[60px] line-clamp-3">
              {{ truncatedDescription }}
            </p>

          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useFormatters } from '../composables/useFormatters';
import FavoriteButton from './FavoriteButton.vue';

const props = defineProps({
  manga: {
    type: Object,
    required: true
  },
  isFavorite: {
    type: Boolean,
    default: false
  },
  activeGenre: {
    type: String,
    default: ''
  },
  allowGenreFilter: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['toggleFavorite', 'selectGenre']);

const { getChapterID, truncateDescription } = useFormatters();

const chapterId = computed(() => getChapterID(props.manga.latestChapter));
const truncatedDescription = computed(() => truncateDescription(props.manga.description));
</script>

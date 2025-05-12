    <template>
    <div
        class="border-2 border-gray-300 rounded-lg shadow-xl bg-white overflow-hidden flex flex-col mb-8"
        style="box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);"
    >
        <div class="relative">
        <!-- Favorite Button -->
        <FavoriteButton 
            :is-favorite="isFavorite" 
            @toggle="$emit('toggleFavorite')"
        />

        <router-link :to="{ name: 'mangaDetail', params: { mangaId: mangaId } }">
            <!-- Image -->
            <div class="h-64 w-full" style="min-height: 250px;">
            <img
                :src="imageSrc"
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
                    <span class="text-sm">{{ chapterId }}</span>
                </div>
                <div>
                    <span class="text-sm font-medium text-gray-500">Views:</span>
                    <span class="text-sm">{{ manga.views }}</span>
                </div>
                </div>

                <!-- Description -->
                <p class="text-sm text-gray-600 mb-3 min-h-[60px] line-clamp-3">
                {{ truncatedDescription }}
                </p>

                <!-- Genres container -->
                <div class="flex flex-wrap gap-2 mb-3 flex-grow-0">
                <GenreTag
                    v-for="(genre, index) in manga.genres"
                    :key="index"
                    :genre="genre"
                    :is-active="activeGenre === genre"
                    :interactive="allowGenreFilter"
                    @click="$emit('selectGenre', genre)"
                />
                </div>
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
    import GenreTag from './GenreTag.vue';

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

    const { getImageSrc, getMangaID, getChapterID, truncateDescription } = useFormatters();

    const mangaId = computed(() => getMangaID(props.manga.latestChapter));
    const chapterId = computed(() => getChapterID(props.manga.latestChapter));
    const imageSrc = computed(() => getImageSrc(props.manga.img_path));
    const truncatedDescription = computed(() => truncateDescription(props.manga.description));
    </script>
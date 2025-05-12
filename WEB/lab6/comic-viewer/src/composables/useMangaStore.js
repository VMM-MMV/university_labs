import { ref, computed, onMounted } from 'vue';

export function useMangaStore() {
  const mangaList = ref([]);
  const isLoading = ref(true);
  const error = ref(null);

  // Load all manga
  const loadMangaList = async () => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await fetch('/manga_store/store.json');
      if (response.ok) {
        mangaList.value = await response.json();
      } else {
        error.value = `Failed to load manga list: ${response.statusText}`;
        console.error(error.value);
      }
    } catch (err) {
      error.value = `Error loading manga list: ${err.message}`;
      console.error(error.value, err);
    } finally {
      isLoading.value = false;
    }
  };

  // Load single manga details
  const loadMangaDetails = async (mangaId) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await fetch(`/manga_store/contents/${mangaId}/info.json`);
      if (response.ok) {
        return await response.json();
      } else {
        error.value = `Failed to load manga details: ${response.statusText}`;
        console.error(error.value);
        return null;
      }
    } catch (err) {
      error.value = `Error loading manga details: ${err.message}`;
      console.error(error.value, err);
      return null;
    } finally {
      isLoading.value = false;
    }
  };

  // Load chapter images
  const loadChapterImages = async (mangaId, chapterName) => {
    isLoading.value = true;
    error.value = null;
    const images = [];
    
    try {
      let index = 0;
      while (true) {
        const imagePath = `/manga_store/contents/${mangaId}/${chapterName}/${index}.webp`;
        // Try to fetch the image HEAD (lightweight check)
        const response = await fetch(imagePath, { method: 'HEAD' });
        if (response.ok) {
          images.push(imagePath);
          index++;
        } else {
          // No more images found
          break;
        }
      }
      return images;
    } catch (err) {
      error.value = `Error loading chapter images: ${err.message}`;
      console.error(error.value, err);
      return images;
    } finally {
      isLoading.value = false;
    }
  };

  // Get all unique genres across all manga
  const allGenres = computed(() => {
    const genres = new Set();
    mangaList.value.forEach(manga => {
      if (manga.genres && Array.isArray(manga.genres)) {
        manga.genres.forEach(genre => genres.add(genre));
      }
    });
    return Array.from(genres).sort();
  });

  // Initialize on component mount
  onMounted(() => {
    loadMangaList();
  });

  return {
    mangaList,
    isLoading,
    error,
    allGenres,
    loadMangaList,
    loadMangaDetails,
    loadChapterImages
  };
}
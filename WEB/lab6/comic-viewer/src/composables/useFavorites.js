import { ref, onMounted } from 'vue';
import { useFormatters } from './useFormatters';

export function useFavorites() {
  const favorites = ref([]);
  const { getMangaID } = useFormatters();

  // Load favorites from localStorage
  const loadFavorites = () => {
    const storedFavorites = localStorage.getItem('mangaFavorites');
    if (storedFavorites) {
      favorites.value = JSON.parse(storedFavorites);
    }
  };

  // Save favorites to localStorage
  const saveFavorites = () => {
    localStorage.setItem('mangaFavorites', JSON.stringify(favorites.value));
  };

  // Toggle favorite status for a manga
  const toggleFavorite = (manga) => {
    const mangaId = getMangaID(manga.latestChapter);
    const index = favorites.value.findIndex(id => id === mangaId);
    
    if (index === -1) {
      favorites.value.push(mangaId);
    } else {
      favorites.value.splice(index, 1);
    }
    
    saveFavorites();
  };

  // Remove manga from favorites
  const removeFromFavorites = (manga) => {
    const mangaId = getMangaID(manga.latestChapter);
    const index = favorites.value.findIndex(id => id === mangaId);
    
    if (index !== -1) {
      favorites.value.splice(index, 1);
      saveFavorites();
    }
  };

  // Check if manga is in favorites
  const isFavorite = (manga) => {
    const mangaId = getMangaID(manga.latestChapter);
    return favorites.value.includes(mangaId);
  };

  // Initialize favorites on component mount
  onMounted(() => {
    loadFavorites();
  });

  return {
    favorites,
    toggleFavorite,
    removeFromFavorites,
    isFavorite,
    loadFavorites
  };
}
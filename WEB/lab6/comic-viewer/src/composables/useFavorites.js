import { ref, onMounted } from 'vue';

export function useFavorites() {
  const favorites = ref([]);

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
    const index = favorites.value.findIndex(id => id === manga.mangaID);
    
    if (index === -1) {
      favorites.value.push(manga.mangaID);
    } else {
      favorites.value.splice(index, 1);
    }
    
    saveFavorites();
  };

  // Remove manga from favorites
  const removeFromFavorites = (manga) => {
    const index = favorites.value.findIndex(id => id === manga.mangaID);
    
    if (index !== -1) {
      favorites.value.splice(index, 1);
      saveFavorites();
    }
  };

  // Check if manga is in favorites
  const isFavorite = (manga) => {
    return favorites.value.includes(manga.mangaID);
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
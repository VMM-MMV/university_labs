import { ref, onMounted } from 'vue';
import { authFetch } from './authFetch.js';

export function useRestStore() {
  const mangaList = ref([]);
  const isLoading = ref(true);
  const error = ref(null);

  // Load all manga (latest releases)
  const loadMangaList = async (page = 1) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await authFetch(`/api/mangas/?page=${page}`);
      if (response.ok) {
        const data = await response.json();
        // The API returns results array where the last item contains pagination info
        if (data.results && Array.isArray(data.results) && data.results.length > 0) {
          // Process manga items (all except the last one)
          const mangaItems = data.results.slice(0, -1).map(manga => ({
            ...manga,
            img: manga.img ? getImageUrl(manga.img) : null,
          }));
          
          mangaList.value = mangaItems;
        } else {
          mangaList.value = [];
        }
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

  // Search manga
  const searchManga = async (query, page = 1) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await authFetch(`/api/mangas/search?query=${encodeURIComponent(query)}&page=${page}`);
      if (response.ok) {
        const data = await response.json();
        // Add pagination info
        let paginationInfo = {};
        if (data.pages && Array.isArray(data.pages) && data.pages.length > 0) {
          paginationInfo = data.pages[0];
        }
        
        // Process manga items
        const processedResults = (data.results || []).map(manga => ({
          ...manga,
          img: manga.img ? getImageUrl(manga.img) : null,
        }));
        
        return {
          mangas: processedResults,
          pagination: paginationInfo
        };
      } else {
        error.value = `Failed to search manga: ${response.statusText}`;
        console.error(error.value);
        return { mangas: [], pagination: {} };
      }
    } catch (err) {
      error.value = `Error searching manga: ${err.message}`;
      console.error(error.value, err);
      return { mangas: [], pagination: {} };
    } finally {
      isLoading.value = false;
    }
  };

  // Load manga details
  const loadMangaDetails = async (mangaId) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await authFetch(`/api/mangas/${mangaId}`);
      if (response.ok) {
        const data = await response.json();
        
        if (data.results) {
          const mangaData = data.results;
          
          // Process manga cover image
          const processedManga = {
            ...mangaData,
            img: mangaData.img ? getImageUrl(mangaData.img) : null,
            
            // Process chapters if present
            chapters: Array.isArray(mangaData.chapters) ? mangaData.chapters.map(chapter => ({
              ...chapter,
              id: chapter.chapterID,
              name: chapter.chapterName
            })) : []
          };
          
          return processedManga;
        }
        
        return null;
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

  // Load chapter data
  const loadChapter = async (chapterPath) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await authFetch(`/api/mangas/chapter/${chapterPath}`);
      if (response.ok) {
        const data = await response.json();
        
        if (data.results) {
          const chapterData = data.results;
          
          return {
            ...chapterData,
            title: chapterData.title || '',
            // We'll process the image URLs when they're requested in loadChapterImages
            primaryImages: chapterData.primary_imgs || [],
            secondaryImages: chapterData.secondary_imgs || [],
            availableChapters: chapterData.chapters || [],
            currentChapter: chapterData.currentChapter || ''
          };
        }
        
        return null;
      } else {
        error.value = `Failed to load chapter: ${response.statusText}`;
        console.error(error.value);
        return null;
      }
    } catch (err) {
      error.value = `Error loading chapter: ${err.message}`;
      console.error(error.value, err);
      return null;
    } finally {
      isLoading.value = false;
    }
  };

  // Get image URL for downloading
  const getImageUrl = (imageUrl, referer = "https://www.mangakakalot.gg/") => {
    // Encode the URL and referer parameters
    const encodedUrl = encodeURIComponent(imageUrl);
    const encodedReferer = encodeURIComponent(referer);
    
    // Return the constructed URL to the image download endpoint
    return `/api/images/download?url=${encodedUrl}&referer=${encodedReferer}`;
  };

  // Load chapter images
  const loadChapterImages = async (chapterPath, onImageLoaded) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Load the chapter data
      const chapterData = await loadChapter(chapterPath);
      
      if (chapterData) {
        // First try primary images
        if (chapterData.primaryImages && chapterData.primaryImages.length > 0) {
          chapterData.primaryImages.forEach((imageUrl, index) => {
            // Get the download URL for the image
            const downloadUrl = getImageUrl(imageUrl);
            
            // Notify the caller with the processed image URL
            onImageLoaded(downloadUrl, index);
          });
          return chapterData.primaryImages.length;
        } 
        // Fall back to secondary images if available and primary is empty
        else if (chapterData.secondaryImages && chapterData.secondaryImages.length > 0) {
          chapterData.secondaryImages.forEach((imageUrl, index) => {
            // Get the download URL for the image
            const downloadUrl = getImageUrl(imageUrl);
            
            // Notify the caller with the processed image URL
            onImageLoaded(downloadUrl, index);
          });
          return chapterData.secondaryImages.length;
        }
      }
      
      return 0;
    } catch (err) {
      error.value = `Error loading chapter images: ${err.message}`;
      console.error(error.value, err);
      return 0;
    } finally {
      isLoading.value = false;
    }
  };

  // Initialize on component mount
  onMounted(() => {
    loadMangaList();
  });

  return {
    mangaList,
    isLoading,
    error,
    loadMangaList,
    searchManga,
    loadMangaDetails,
    loadChapter,
    loadChapterImages,
    getImageUrl
  };
}
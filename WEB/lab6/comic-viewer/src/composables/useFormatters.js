export function useFormatters() {
  // Extract chapter ID from chapter path
  const getChapterID = (chapterPath) => {
    if (!chapterPath) return '';
    const parts = chapterPath.split(/[\\\/]/); // Handle both backslash and forward slash
    return parts[parts.length - 1];
  };

  // Extract manga ID from chapter path
  const getMangaID = (chapterPath) => {
    if (!chapterPath) return '';
    const parts = chapterPath.split(/[\\\/]/); // Handle both backslash and forward slash
    return parts[parts.length - 2];
  };

  // Get image source with fallback
  const getImageSrc = (imgPath) => {
    return imgPath || '/api/placeholder/400/640';
  };

  // Truncate and clean description
  const truncateDescription = (desc, maxLength = 200) => {
    if (!desc) return '';
    // Remove common boilerplate text
    const cleanDesc = desc.replace(/You are reading.*?bookmark\.\n\n\s+/s, '');
    if (cleanDesc.length > maxLength) {
      return cleanDesc.substring(0, maxLength) + '...';
    }
    return cleanDesc;
  };

  return {
    getChapterID,
    getMangaID,
    getImageSrc,
    truncateDescription
  };
}
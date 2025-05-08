import axios from 'axios';

class ImageProxyService {
  constructor() {
    this.axios = axios.create({
      timeout: 10000
    });
  }
  
  /**
   * Proxy an image request with proper headers to avoid CORS and referrer blocks
   * @param {string} url - URL of the image to proxy
   * @returns {Promise<Blob>} - Image blob
   */
  async fetchImageWithHeaders(url) {
    try {
      // Extract the original URL from the query param if it exists
      const urlToFetch = url.includes('?withHeaders=true') 
        ? url.replace('?withHeaders=true', '')
        : url;
      
      const response = await this.axios.get(urlToFetch, {
        responseType: 'blob',
        headers: {
          "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
          "Referer": "https://www.mangakakalot.gg/",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Error fetching image:', error);
      throw error;
    }
  }
  
  /**
   * Create a data URL from an image blob
   * @param {Blob} blob - Image blob
   * @returns {Promise<string>} - Data URL
   */
  async blobToDataUrl(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }
}

// Create and export a singleton instance
const imageProxy = new ImageProxyService();
export default imageProxy;
<template>
    <div class="manga-image-container">
      <img
        v-if="imageUrl && !needsProxy"
        :src="imageUrl"
        :alt="alt"
        class="manga-image"
        @error="handleImageError"
        ref="imgEl"
      />
      <img
        v-else-if="proxiedImageUrl"
        :src="proxiedImageUrl"
        :alt="alt"
        class="manga-image"
        ref="proxiedImgEl"
      />
      <div v-else-if="loading" class="image-loading">
        <div class="spinner"></div>
      </div>
      <div v-else-if="error" class="image-error">
        <span>Failed to load image</span>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from 'vue';
  import imageProxy from './ImageProxyService';

  // eslint-disable-next-line no-undef
  const props = defineProps({
    src: {
      type: String,
      required: true
    },
    alt: {
      type: String,
      default: 'Manga image'
    },
    fallbackSrc: {
      type: String,
      default: '/api/placeholder/200/300'
    }
  });
  
  const imgEl = ref(null);
  const proxiedImgEl = ref(null);
  const loading = ref(false);
  const error = ref(false);
  const proxiedImageUrl = ref(null);
  
  // Determine if image needs proxy based on URL
  const needsProxy = computed(() => {
    return props.src && (
      props.src.includes('?withHeaders=true') ||
      props.src.includes('2xstorage.com')
    );
  });
  
  // Clean version of the image URL without our query parameters
  const imageUrl = computed(() => {
    if (!props.src) return null;
    return props.src.replace('?withHeaders=true', '');
  });
  
  // Function to handle image loading errors
  const handleImageError = async () => {
    if (props.src && !needsProxy.value) {
      // If regular image fails, try proxy
      await proxyImage(props.src);
    } else if (props.fallbackSrc) {
      // If proxied image fails, use fallback
      error.value = true;
      proxiedImageUrl.value = props.fallbackSrc;
    }
  };
  
  // Function to load image via proxy
  const proxyImage = async (url) => {
    if (!url) return;
    
    loading.value = true;
    error.value = false;
    
    try {
      const imageBlob = await imageProxy.fetchImageWithHeaders(url);
      const dataUrl = await imageProxy.blobToDataUrl(imageBlob);
      proxiedImageUrl.value = dataUrl;
    } catch (err) {
      console.error('Failed to proxy image:', err);
      error.value = true;
      proxiedImageUrl.value = props.fallbackSrc;
    } finally {
      loading.value = false;
    }
  };
  
  // Watch for changes to src prop
  watch(() => props.src, (newSrc) => {
    if (newSrc && needsProxy.value) {
      proxyImage(newSrc);
    } else {
      // Reset state for regular images
      proxiedImageUrl.value = null;
      error.value = false;
    }
  });
  
  onMounted(() => {
    if (props.src && needsProxy.value) {
      proxyImage(props.src);
    }
  });
  </script>
  
  <style scoped>
  .manga-image-container {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: #f0f0f0;
  }
  
  .manga-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .image-loading, .image-error {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }
  
  .spinner {
    width: 30px;
    height: 30px;
    border: 3px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top-color: #3f51b5;
    animation: spin 1s ease-in-out infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .image-error {
    background-color: #f8d7da;
    color: #721c24;
    font-size: 0.9rem;
    text-align: center;
    padding: 5px;
  }
</style>
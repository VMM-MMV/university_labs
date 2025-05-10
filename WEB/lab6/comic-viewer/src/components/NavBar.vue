<template>
  <nav class="bg-gray-800 p-4 sticky top-0 z-10">
    <div class="flex justify-between">
      <div class="space-x-4 pl-10">
        <router-link to="/" class="text-white hover:text-green-400">Home</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>
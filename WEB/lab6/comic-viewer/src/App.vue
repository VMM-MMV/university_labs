<template>
  <NavBar />
  <router-view />
</template>

<script>
import MainPage from './views/MainPage.vue'
import NavBar from './views/Navbar.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    MainPage
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>

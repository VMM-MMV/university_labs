<template>
  <NavBar />
  <router-view />
</template>

<script>
import MainPage from './components/MainPage.vue'
import NavBar from './components/Navbar.vue'

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

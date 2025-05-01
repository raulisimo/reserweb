<template>
  <footer class="footer bg-dark text-light text-center py-3 mt-5">
    <p>&copy; {{ currentYear }} Reserweb. Todos los derechos reservados.</p>
  </footer>
</template>

<script setup>
import { ref } from 'vue'

const currentYear = ref(new Date().getFullYear())
</script>

<style scoped>
.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
}

body,
html {
  height: 100%;
  margin: 0;
}

#app {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

footer {
  margin-top: auto; /* Ensures the footer sticks to the bottom */
}
</style>

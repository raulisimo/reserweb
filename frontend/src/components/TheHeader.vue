<template>
  <header class="bg-dark py-3 shadow-sm">
    <nav class="container d-flex justify-content-between align-items-center">
      <a href="/" class="text-decoration-none">
        <h1 class="text-light m-0">🍽️ Reserweb</h1>
      </a>

      <ul class="nav align-items-center gap-2">
        <li class="nav-item">
          <a class="nav-link text-light" href="/">Inicio</a>
        </li>
        <li class="nav-item">
          <a class="btn btn-outline-light" href="/restaurants">Restaurantes</a>
        </li>
        <li class="nav-item">
          <a class="btn btn-outline-light" href="/reviews">Reseñas</a>
        </li>
        <li class="nav-item">
          <a class="btn btn-primary text-light" href="/book">Reserva ya</a>
        </li>

        <!-- Authenticated User Menu -->
        <li class="nav-item dropdown position-relative" ref="dropdownRef">
          <button class="btn btn-outline-light dropdown-toggle" @click="toggleDropdown">
            <span v-if="isAuthenticated">Hola, {{ user?.name }}!</span>
            <span v-else>Acceso</span>
          </button>

          <ul class="dropdown-menu show mt-2" v-show="showDropdown">
            <template v-if="!isAuthenticated">
              <li><a class="dropdown-item" href="/login">Iniciar sesión</a></li>
              <li><a class="dropdown-item" href="/signup">Registrarse</a></li>
            </template>

            <template v-if="isAdmin">
              <li><a class="dropdown-item" href="/admin">Panel de Admin</a></li>
              <li>
                <a class="dropdown-item text-danger" href="#" @click.prevent="logout"
                  >Cerrar sesión</a
                >
              </li>
            </template>

            <template v-if="isClient">
              <li><a class="dropdown-item" href="/my-reviews">Mis Reseñas</a></li>
              <li><a class="dropdown-item" href="/profile">Mi Perfil</a></li>
              <li>
                <a class="dropdown-item text-danger" href="#" @click.prevent="logout"
                  >Cerrar sesión</a
                >
              </li>
            </template>

            <template v-if="isRestaurant">
              <li><a class="dropdown-item" href="/profile">Mi Perfil</a></li>
              <li><a class="dropdown-item" href="/my-bookings">Mis Reservas</a></li>
              <li>
                <a class="dropdown-item text-danger" href="#" @click.prevent="logout"
                  >Cerrar sesión</a
                >
              </li>
            </template>
          </ul>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const showDropdown = ref(false)
const dropdownRef = ref(null)

const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)
const isAdmin = computed(() => authStore.isAdmin)
const isClient = computed(() => authStore.isClient)
const isRestaurant = computed(() => authStore.isRestaurant)

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showDropdown.value = false
  }
}

onMounted(() => {
  // eslint-disable-next-line no-undef
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  // eslint-disable-next-line no-undef
  document.removeEventListener('click', handleClickOutside)
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dropdown-menu {
  display: block;
  min-width: 200px;
  background-color: #212529;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 0;
  position: absolute;
  z-index: 1000;
}

.dropdown-item {
  color: #fff;
}

.dropdown-item:hover {
  background-color: #007bff;
  color: #fff;
}
</style>

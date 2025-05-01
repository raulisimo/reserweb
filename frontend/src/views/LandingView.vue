<template>
  <div>
    <BaseLayout>
      <section class="text-center py-5 bg-dark text-light">
        <div class="container">
          <h1 class="display-3 fw-bold mb-3 animate__animated animate__fadeInDown">
            Descubre y reserva los mejores restaurantes
          </h1>
          <p class="lead mb-4 animate__animated animate__fadeInUp">
            Encuentra la mejor comida, exclusivos descuentos y opiniones verificadas
          </p>
          <div
            class="d-flex flex-column flex-md-row justify-content-center animate__animated animate__fadeInUp"
          >
            <input
              v-model="searchQuery"
              class="form-control w-100 w-md-50 me-md-2 mb-2 mb-md-0"
              type="search"
              placeholder="Busca restaurantes..."
              @input="fetchRestaurants"
            />
            <button class="btn btn-primary px-4" @click="searchRestaurants">Buscar</button>
          </div>

          <!-- Search Results -->
          <div v-if="restaurants.length > 0" class="mt-3">
            <ul class="list-group">
              <li
                v-for="restaurant in restaurants"
                :key="restaurant.id"
                class="list-group-item list-group-item-action"
                @click="goToRestaurantDetail(restaurant.id)"
              >
                {{ restaurant.name }} - {{ restaurant.address }}
              </li>
            </ul>
          </div>
          <p v-if="searched && restaurants.length === 0" class="mt-4">
            No se han encontrado restaurantes
          </p>
        </div>
      </section>

      <Carousel />
      <CustomerReviews />
    </BaseLayout>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { searchRestaurants } from '@/services/restaurantService'

import BaseLayout from '@/views/layouts/BaseLayout.vue'

import Carousel from '@/components/ImageCarousel.vue'
import CustomerReviews from '@/components/CustomerReviews.vue'

const searchQuery = ref('')
const restaurants = ref([])
const searched = ref(false)

const router = useRouter()

const fetchRestaurants = async () => {
  if (searchQuery.value.trim()) {
    try {
      searched.value = true
      restaurants.value = await searchRestaurants(searchQuery.value)
    } catch (error) {
      console.error('Error fetching restaurants:', error)
    }
  } else {
    restaurants.value = []
    searched.value = false
  }
}

const goToRestaurantDetail = (id) => {
  router.push(`/restaurant/${id}`)
}
</script>

<style></style>

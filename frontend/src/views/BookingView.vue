<template>
  <main>
    <BaseLayout>
      <div class="container py-5">
        <h2 class="mb-4 text-center">Reserva en tu restaurante favorito</h2>

        <!-- ✅ Success message -->
        <div v-if="successMessage" class="alert alert-success text-center">
          {{ successMessage }}
        </div>

        <!-- 📋 Booking Form -->
        <form @submit.prevent="submitBooking" class="card p-4 shadow-sm">
          <!-- 🔍 Searchable Restaurant Input -->
          <div class="mb-3 position-relative">
            <label class="form-label">Restaurante</label>
            <input
              type="text"
              class="form-control"
              v-model="restaurantSearch"
              @input="onSearchInput"
              @focus="onFocus"
              @blur="hideSuggestionsWithDelay"
              placeholder="Buscar restaurante por nombre"
              autocomplete="off"
              required
            />
            <ul
              v-if="showSuggestions && searchResults.length"
              class="list-group position-absolute w-100 z-3 shadow"
              style="max-height: 200px; overflow-y: auto"
            >
              <li
                class="list-group-item list-group-item-action"
                v-for="r in searchResults"
                :key="r.id"
                @mousedown.prevent="selectRestaurant(r)"
              >
                {{ r.name }}
              </li>
            </ul>
            <div
              v-else-if="showSuggestions"
              class="text-muted small position-absolute mt-1"
              style="z-index: 3"
            >
              No se encontraron restaurantes.
            </div>
          </div>

          <!-- 📅 Date Picker -->
          <div class="mb-3">
            <label class="form-label">Fecha</label>
            <input type="date" class="form-control" v-model="bookingDate" :min="today" required />
          </div>

          <!-- ⏰ Time Picker -->
          <div class="mb-3">
            <label class="form-label">Hora</label>
            <input type="time" class="form-control" v-model="bookingTime" :min="minTime" required />
          </div>

          <!-- 👥 Number of People -->
          <div class="mb-3">
            <label class="form-label">Número de personas</label>
            <input
              type="number"
              class="form-control"
              v-model.number="numberOfPeople"
              min="1"
              required
            />
          </div>

          <!-- 📝 Special Requests -->
          <div class="mb-3">
            <label class="form-label">Comentarios (alergias, etc.)</label>
            <textarea
              v-model="specialRequest"
              class="form-control"
              rows="3"
              placeholder="¿Alguna petición especial?"
            ></textarea>
          </div>

          <!-- ✅ Submit -->
          <div>
            <button type="submit" class="btn btn-primary w-100">Reservar</button>
          </div>
        </form>
      </div>
    </BaseLayout>
  </main>
</template>

<script setup>
import { ref, computed } from 'vue'
import BaseLayout from '@/views/layouts/BaseLayout.vue'
import { searchRestaurants } from '@/services/restaurantService.js'
import { createBooking } from '@/services/bookingService.js'

const restaurantSearch = ref('')
const selectedRestaurant = ref(null)
const searchResults = ref([])
const showSuggestions = ref(false)

const bookingDate = ref('')
const bookingTime = ref('')
const numberOfPeople = ref(1)
const specialRequest = ref('')
const successMessage = ref('')

const today = new Date().toISOString().split('T')[0]

const minTime = computed(() => {
  const now = new Date()
  const selectedDate = new Date(bookingDate.value)
  if (bookingDate.value === today && selectedDate.toDateString() === now.toDateString()) {
    const h = now.getHours().toString().padStart(2, '0')
    const m = now.getMinutes().toString().padStart(2, '0')
    return `${h}:${m}`
  }
  return '00:00'
})

const onSearchInput = async () => {
  showSuggestions.value = true
  await fetchRestaurants(restaurantSearch.value)
}

const onFocus = async () => {
  showSuggestions.value = true
  if (searchResults.value.length === 0) await fetchRestaurants('')
}

const hideSuggestionsWithDelay = () => {
  setTimeout(() => (showSuggestions.value = false), 150)
}

const selectRestaurant = (restaurant) => {
  selectedRestaurant.value = restaurant
  restaurantSearch.value = restaurant.name
  showSuggestions.value = false
}

const fetchRestaurants = async (query = '') => {
  try {
    const result = await searchRestaurants(query)
    searchResults.value = result
  } catch (err) {
    console.error('Error fetching restaurants:', err)
    searchResults.value = []
  }
}

const resetForm = () => {
  restaurantSearch.value = ''
  selectedRestaurant.value = null
  bookingDate.value = ''
  bookingTime.value = ''
  numberOfPeople.value = 1
  specialRequest.value = ''
}

const submitBooking = async () => {
  if (!selectedRestaurant.value) {
    // eslint-disable-next-line no-undef
    alert('Por favor selecciona un restaurante de la lista.')
    return
  }

  const fullDateTime = new Date(`${bookingDate.value}T${bookingTime.value}`)
  const bookingData = {
    restaurant_id: selectedRestaurant.value.id,
    booking_time: fullDateTime.toISOString(),
    number_of_people: numberOfPeople.value,
    special_request: specialRequest.value,
  }

  try {
    await createBooking(bookingData)
    successMessage.value = '¡Reserva realizada con éxito!'
    resetForm()
  } catch (err) {
    console.error('Error creating booking:', err)
  }
}
</script>

<style scoped>
form {
  max-width: 600px;
  margin: auto;
}

.list-group-item {
  cursor: pointer;
}
</style>

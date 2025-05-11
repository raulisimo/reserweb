<template>
  <main>
    <BaseLayout>
      <div class="container mx-auto py-6">
        <h2 class="text-2xl font-semibold mb-4 text-center">Reservas del Restaurante</h2>

        <div v-if="loading" class="text-center text-gray-500">Cargando reservas...</div>
        <div v-else>
          <!-- Pending Bookings -->
          <section class="mb-8">
            <h3 class="text-xl font-bold mb-2">Pendientes</h3>
            <div v-if="pendingBookings.length" class="grid gap-4 md:grid-cols-2">
              <BookingCard
                v-for="booking in pendingBookings"
                :key="booking.id"
                :booking="booking"
              />
            </div>
            <div v-else class="text-gray-500">No hay reservas pendientes.</div>
          </section>

          <!-- Past Bookings -->
          <section>
            <h3 class="text-xl font-bold mb-2">Pasadas</h3>
            <div v-if="pastBookings.length" class="grid gap-4 md:grid-cols-2">
              <BookingCard
                v-for="booking in pastBookings"
                :key="booking.id"
                :booking="booking"
              />
            </div>
            <div v-else class="text-gray-500">No hay reservas pasadas.</div>
          </section>
        </div>

        <div v-if="error" class="text-red-600 text-center mt-4">{{ error }}</div>
      </div>
    </BaseLayout>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BaseLayout from '@/views/layouts/BaseLayout.vue'
import BookingCard from '@/components/BookingCard.vue'
import { getBookingsByRestaurant } from '@/services/bookingService'

const pendingBookings = ref([])
const pastBookings = ref([])
const loading = ref(true)
const error = ref(null)

const loadBookings = async () => {
  try {
    const bookings = await getBookingsByRestaurant()
    const now = new Date()

    // Filter bookings based on 'booking_time'
    pendingBookings.value = bookings.filter(b => new Date(b.booking_time) >= now)
    pastBookings.value = bookings.filter(b => new Date(b.booking_time) < now)
  } catch (err) {
    error.value = 'Error al cargar reservas.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(loadBookings)
</script>

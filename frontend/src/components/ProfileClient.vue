<template>
  <div class="container py-5">
    <h2 class="mb-4 text-center">Mi Perfil</h2>

    <!-- User Info -->
    <div v-if="user" class="card mb-4 profile-card">
      <div class="card-body">
        <h5 class="card-title">{{ user.name }}</h5>
        <p class="card-text"><strong>Email:</strong> {{ user.email }}</p>
        <p class="card-text"><strong>Teléfono:</strong> {{ user.phone || 'No disponible' }}</p>
      </div>
    </div>

    <!-- Bookings (if available) -->
    <div v-if="userBookings && userBookings.length > 0">
      <h4 class="my-4">Mis Reservas</h4>
      <ul class="list-group booking-list">
        <li v-for="booking in userBookings" :key="booking.id" class="list-group-item booking-item">
          <div class="booking-header">
            <p class="booking-restaurant">
              <strong>Restaurante:</strong> {{ booking.restaurant_name || 'No disponible' }}
            </p>
            <p class="booking-status">
              <span class="badge bg-success">Confirmada</span>
            </p>
          </div>

          <div class="booking-details">
            <p>
              <i class="fas fa-calendar-alt"></i> <strong>Fecha:</strong>
              {{ formatDate(booking.booking_time) }}
            </p>
            <p>
              <i class="fas fa-users"></i> <strong>Personas:</strong> {{ booking.number_of_people }}
            </p>
            <p v-if="booking.special_request">
              <i class="fas fa-comment"></i> <strong>Solicitudes especiales:</strong>
              {{ booking.special_request }}
            </p>
            <p>
              <i class="fas fa-clock"></i> <strong>Creado el:</strong>
              {{ formatDate(booking.created_at) }}
            </p>
          </div>

          <div class="booking-actions">
            <button @click="deleteBooking(booking.id)" class="btn btn-danger btn-sm">
              Eliminar
            </button>
          </div>
        </li>
      </ul>
    </div>

    <div v-else-if="isLoading" class="loading-state">
      <p><i class="fas fa-spinner fa-spin"></i> Cargando reservas...</p>
    </div>

    <div v-else class="empty-state">
      <p>No tienes reservas en este momento.</p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { getBookingsByClient, deleteBookingByUser } from '@/services/bookingService'

// Store and router
const authStore = useAuthStore()
const router = useRouter()

// Data
const user = computed(() => authStore.user)
const userBookings = ref([])
const isLoading = ref(true)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
  } else {
    try {
      const bookingsResponse = await getBookingsByClient()
      userBookings.value = bookingsResponse
    } catch (error) {
      console.error('Error fetching bookings:', error)
    } finally {
      isLoading.value = false
    }
  }
})

const deleteBooking = async (bookingId) => {
  try {
    await deleteBookingByUser(bookingId)
    userBookings.value = userBookings.value.filter((booking) => booking.id !== bookingId)
    // eslint-disable-next-line no-undef
    alert('Reserva eliminada exitosamente')
  } catch (error) {
    console.error('Error deleting booking:', error)
    // eslint-disable-next-line no-undef
    alert('Error al eliminar la reserva')
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'Fecha no disponible'

  try {
    const date = new Date(dateString)
    return date.toLocaleString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch (e) {
    console.error('Error formatting date:', e)
    return dateString
  }
}
</script>

<style scoped>
/* Card Styling */
.profile-card {
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: none;
  background-color: #fff;
}

.card-body {
  background-color: #f8f9fa;
  padding: 20px;
}

.card-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #343a40;
}

.card-text {
  font-size: 1rem;
  color: #6c757d;
}

/* Booking Item Styling */
.booking-item {
  border: 1px solid #ddd;
  margin-bottom: 15px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.booking-item:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.booking-status {
  font-size: 0.9rem;
}

.booking-details {
  margin-top: 15px;
}

.booking-actions {
  margin-top: 15px;
  text-align: right;
}

/* Icons */
.fas {
  margin-right: 5px;
}

/* Loading and Empty State */
.loading-state {
  text-align: center;
  font-size: 1.2rem;
  color: #007bff;
}

.empty-state {
  text-align: center;
  font-size: 1.2rem;
  color: #6c757d;
  font-style: italic;
}

/* Button Styling */
.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

/* Responsive Design */
@media (max-width: 768px) {
  .container {
    padding-left: 15px;
    padding-right: 15px;
  }

  .card-body {
    padding: 15px;
  }

  .card-title {
    font-size: 1.2rem;
  }
}
</style>

<template>
  <div class="card shadow-sm rounded-lg border mb-4">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="card-title mb-0">{{ booking.user_name }}</h5>
        <span
          class="badge"
          :class="{
            'bg-warning text-dark': isPending,
            'bg-secondary text-white': !isPending,
          }"
        >
          {{ isPending ? 'Pendiente' : 'Pasada' }}
        </span>
      </div>
      <p class="card-text text-muted mb-2"><strong>Restaurante:</strong> {{ booking.restaurant_name }}</p>
      <p class="card-text text-muted mb-2"><strong>Fecha:</strong> {{ formatDate(booking.booking_time) }}</p>
      <p class="card-text text-muted mb-2"><strong>Hora:</strong> {{ formatTime(booking.booking_time) }}</p>
      <p class="card-text text-muted mb-2"><strong>Personas:</strong> {{ booking.number_of_people }}</p>
      <p v-if="booking.special_request" class="card-text text-muted mb-2"><strong>Petición especial:</strong> {{ booking.special_request }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  booking: {
    type: Object,
    required: true,
  },
})

const isPending = computed(() => new Date(props.booking.booking_time) >= new Date())

const formatDate = (dateStr) => {
  const options = { day: '2-digit', month: 'short', year: 'numeric' }
  return new Date(dateStr).toLocaleDateString('es-ES', options)
}

const formatTime = (dateStr) => {
  const options = { hour: '2-digit', minute: '2-digit' }
  return new Date(dateStr).toLocaleTimeString('es-ES', options)
}
</script>

<style scoped>
.card {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.1rem;
  font-weight: bold;
}

.card-text {
  font-size: 0.875rem;
}

.badge {
  font-size: 0.875rem;
  padding: 0.5rem 0.75rem;
}

.card-body {
  padding: 1.5rem;
}
</style>

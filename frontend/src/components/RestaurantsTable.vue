<template>
  <div class="restaurant-management">
    <h2 class="mb-4">Gestión de Restaurantes</h2>

    <!-- Alert -->
    <div v-if="alert.message" :class="`alert alert-${alert.type}`">{{ alert.message }}</div>

    <!-- Loading -->
    <div v-if="loading" class="d-flex align-items-center mb-3">
      <span class="spinner-border text-primary me-2" role="status"></span>
      <span>Cargando restaurantes...</span>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <button class="btn btn-success mb-3" @click="showAddForm = !showAddForm">
      {{ showAddForm ? 'Cancelar' : 'Añadir Restaurante' }}
    </button>

    <!-- Add Form -->
    <div v-if="showAddForm" class="card p-3 mb-4">
      <form @submit.prevent="handleAdd">
        <input
          v-model="newRestaurant.name"
          class="form-control mb-2"
          placeholder="Nombre"
          required
        />
        <input
          v-model="newRestaurant.email"
          class="form-control mb-2"
          type="email"
          placeholder="Email"
          required
        />
        <input v-model="newRestaurant.phone" class="form-control mb-2" placeholder="Teléfono" />
        <input v-model="newRestaurant.address" class="form-control mb-2" placeholder="Dirección" />
        <textarea
          v-model="newRestaurant.description"
          class="form-control mb-2"
          placeholder="Descripción"
        ></textarea>
        <input
          v-model="newRestaurant.embedded_map"
          class="form-control mb-3"
          placeholder="Mapa embebido (iframe link)"
        />
        <button type="submit" class="btn btn-primary">Crear</button>
      </form>
    </div>

    <!-- Table -->
    <table v-if="restaurants.length" class="table table-bordered">
      <thead class="table-light">
        <tr>
          <th>Nombre</th>
          <th>Email</th>
          <th>Teléfono</th>
          <th>Dirección</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in restaurants" :key="r.id">
          <td>{{ r.name }}</td>
          <td>{{ r.email }}</td>
          <td>{{ r.phone }}</td>
          <td>{{ r.address }}</td>
          <td>
            <button class="btn btn-sm btn-warning me-2" @click="openEditModal(r)">Editar</button>
            <button class="btn btn-sm btn-danger" @click="confirmDelete(r.id)">Borrar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Edit Modal -->
    <div class="modal fade" id="editModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <form @submit.prevent="handleEdit">
            <div class="modal-header">
              <h5 class="modal-title">Editar Restaurante</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" />
            </div>
            <div class="modal-body">
              <input
                v-model="editRestaurant.name"
                class="form-control mb-2"
                placeholder="Nombre"
                required
              />
              <input
                v-model="editRestaurant.email"
                class="form-control mb-2"
                placeholder="Email"
                required
              />
              <input
                v-model="editRestaurant.phone"
                class="form-control mb-2"
                placeholder="Teléfono"
              />
              <input
                v-model="editRestaurant.address"
                class="form-control mb-2"
                placeholder="Dirección"
              />
              <textarea
                v-model="editRestaurant.description"
                class="form-control mb-2"
                placeholder="Descripción"
              ></textarea>
              <input
                v-model="editRestaurant.embedded_map"
                class="form-control"
                placeholder="Mapa embebido (iframe)"
              />
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                Cancelar
              </button>
              <button type="submit" class="btn btn-primary">Guardar</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirmar eliminación</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" />
          </div>
          <div class="modal-body">¿Seguro que deseas eliminar este restaurante?</div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancelar
            </button>
            <button type="button" class="btn btn-danger" @click="handleDelete">Eliminar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'
import {
  fetchRestaurants,
  createRestaurant,
  updateRestaurant,
  deleteRestaurant,
} from '@/services/restaurantService' // you must implement these

const restaurants = ref([])
const loading = ref(false)
const error = ref(null)
const alert = ref({ message: '', type: '' })

const showAddForm = ref(false)
const newRestaurant = ref({
  name: '',
  email: '',
  phone: '',
  address: '',
  description: '',
  embedded_map: '',
})

const editRestaurant = ref({})
const deleteId = ref(null)

const showAlert = (message, type = 'success') => {
  alert.value = { message, type }
  setTimeout(() => (alert.value = { message: '', type: '' }), 3000)
}

const loadRestaurants = async () => {
  loading.value = true
  error.value = null
  try {
    restaurants.value = await fetchRestaurants()
  } catch (err) {
    console.log(err)
    error.value = 'Error al cargar restaurantes.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRestaurants()
})

const handleAdd = async () => {
  try {
    await createRestaurant(newRestaurant.value)
    showAlert('Restaurante creado exitosamente.')
    newRestaurant.value = {
      name: '',
      email: '',
      phone: '',
      address: '',
      description: '',
      embedded_map: '',
    }
    showAddForm.value = false
    loadRestaurants()
  } catch {
    showAlert('Error al crear restaurante.', 'danger')
  }
}

const openEditModal = (r) => {
  editRestaurant.value = { ...r }
  // eslint-disable-next-line no-undef
  new bootstrap.Modal(document.getElementById('editModal')).show()
}

const handleEdit = async () => {
  try {
    await updateRestaurant(editRestaurant.value.id, editRestaurant.value)
    showAlert('Restaurante actualizado.')
    // eslint-disable-next-line no-undef
    bootstrap.Modal.getInstance(document.getElementById('editModal')).hide()
    loadRestaurants()
  } catch {
    showAlert('Error al actualizar restaurante.', 'danger')
  }
}

const confirmDelete = (id) => {
  deleteId.value = id
  // eslint-disable-next-line no-undef
  new bootstrap.Modal(document.getElementById('deleteModal')).show()
}

const handleDelete = async () => {
  try {
    await deleteRestaurant(deleteId.value)
    showAlert('Restaurante eliminado.')
    // eslint-disable-next-line no-undef
    bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide()
    loadRestaurants()
  } catch {
    showAlert('Error al eliminar restaurante.', 'danger')
  }
}
</script>

<style scoped>
.restaurant-management {
  max-width: 900px;
  margin: auto;
}
</style>

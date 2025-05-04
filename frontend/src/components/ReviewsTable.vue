<template>
  <div class="review-management">
    <h2 class="mb-4">Gestión de Reseñas</h2>

    <!-- Alerts -->
    <div v-if="alert.message" :class="`alert alert-${alert.type}`">{{ alert.message }}</div>

    <!-- Loading -->
    <div v-if="loading" class="d-flex align-items-center mb-3">
      <span class="spinner-border text-primary me-2" role="status"></span>
      <span>Cargando reseñas...</span>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <button class="btn btn-success mb-3" @click="showAddForm = !showAddForm">
      {{ showAddForm ? 'Cancelar' : 'Añadir Reseña' }}
    </button>

    <!-- Add Review Form -->
    <div v-if="showAddForm" class="card p-3 mb-4">
      <form @submit.prevent="handleAdd">
        <input
          v-model="newReview.user_id"
          class="form-control mb-2"
          placeholder="ID de Usuario"
          type="number"
          required
        />
        <input
          v-model="newReview.restaurant_id"
          class="form-control mb-2"
          placeholder="ID de Restaurante"
          type="number"
          required
        />
        <input
          v-model="newReview.rating"
          class="form-control mb-2"
          placeholder="Puntuación (1-5)"
          type="number"
          min="1"
          max="5"
          required
        />
        <textarea
          v-model="newReview.comment"
          class="form-control mb-3"
          placeholder="Comentario"
        ></textarea>
        <button type="submit" class="btn btn-primary">Crear</button>
      </form>
    </div>

    <!-- Reviews Table -->
    <table v-if="reviews.length" class="table table-bordered">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Usuario</th>
          <th>Restaurante</th>
          <th>Puntuación</th>
          <th>Comentario</th>
          <th>Fecha</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in reviews" :key="r.id">
          <td>{{ r.id }}</td>
          <td>{{ r.user_name }}</td>
          <td>{{ r.restaurant_name }}</td>
          <td>{{ r.rating }}</td>
          <td>{{ r.comment }}</td>
          <td>{{ formatDate(r.created_at) }}</td>
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
              <h5 class="modal-title">Editar Reseña</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" />
            </div>
            <div class="modal-body">
              <input
                v-model="editReview.user_id"
                class="form-control mb-2"
                placeholder="ID de Usuario"
                type="number"
                required
              />
              <input
                v-model="editReview.restaurant_id"
                class="form-control mb-2"
                placeholder="ID de Restaurante"
                type="number"
                required
              />
              <input
                v-model="editReview.rating"
                class="form-control mb-2"
                type="number"
                min="1"
                max="5"
                required
              />
              <textarea
                v-model="editReview.comment"
                class="form-control mb-2"
                placeholder="Comentario"
              ></textarea>
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
          <div class="modal-body">¿Seguro que deseas eliminar esta reseña?</div>
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
import { ref, onMounted } from 'vue'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'
import { fetchReviews, createReview, updateReview, deleteReview } from '@/services/reviewService' // you must implement these

const reviews = ref([])
const loading = ref(false)
const error = ref(null)
const alert = ref({ message: '', type: '' })

const showAddForm = ref(false)
const newReview = ref({
  user_id: '',
  restaurant_id: '',
  rating: 5,
  comment: '',
})
const editReview = ref({})
const deleteId = ref(null)

const showAlert = (msg, type = 'success') => {
  alert.value = { message: msg, type }
  setTimeout(() => (alert.value = { message: '', type: '' }), 3000)
}

const formatDate = (iso) => new Date(iso).toLocaleString()

const loadReviews = async () => {
  loading.value = true
  error.value = null
  try {
    reviews.value = await fetchReviews()
  } catch {
    error.value = 'Error al cargar reseñas.'
  } finally {
    loading.value = false
  }
}

onMounted(loadReviews)

const handleAdd = async () => {
  try {
    await createReview(newReview.value)
    showAlert('Reseña creada.')
    showAddForm.value = false
    newReview.value = { user_id: '', restaurant_id: '', rating: 5, comment: '' }
    loadReviews()
  } catch {
    showAlert('Error al crear reseña.', 'danger')
  }
}

const openEditModal = (r) => {
  editReview.value = { ...r }
  // eslint-disable-next-line no-undef
  new bootstrap.Modal(document.getElementById('editModal')).show()
}

const handleEdit = async () => {
  try {
    await updateReview(editReview.value.id, editReview.value)
    showAlert('Reseña actualizada.')
    // eslint-disable-next-line no-undef
    bootstrap.Modal.getInstance(document.getElementById('editModal')).hide()
    loadReviews()
  } catch {
    showAlert('Error al actualizar reseña.', 'danger')
  }
}

const confirmDelete = (id) => {
  deleteId.value = id
  // eslint-disable-next-line no-undef
  new bootstrap.Modal(document.getElementById('deleteModal')).show()
}

const handleDelete = async () => {
  try {
    await deleteReview(deleteId.value)
    showAlert('Reseña eliminada.')
    // eslint-disable-next-line no-undef
    bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide()
    loadReviews()
  } catch {
    showAlert('Error al eliminar reseña.', 'danger')
  }
}
</script>

<style scoped>
.review-management {
  max-width: 1000px;
  margin: auto;
}
</style>

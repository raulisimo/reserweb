<template>
  <div class="user-management">
    <h2 class="mb-4">Gestión de usuarios</h2>

    <!-- Alert messages -->
    <div v-if="alert.message" :class="`alert alert-${alert.type}`">
      {{ alert.message }}
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="d-flex align-items-center mb-3">
      <span class="spinner-border text-primary me-2" role="status" aria-hidden="true"></span>
      <span>Cargando usuarios...</span>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="!loading && users.length === 0" class="alert alert-info">
      No se han encontrado usuarios.
    </div>

    <button class="btn btn-success mb-3" @click="showAddUserForm = !showAddUserForm">
      {{ showAddUserForm ? 'Cancelar' : 'Añadir nuevo usuario' }}
    </button>

    <!-- Add User Form -->
    <div v-if="showAddUserForm" class="card p-3 mb-4">
      <form @submit.prevent="handleAddUser">
        <input v-model="newUser.name" class="form-control mb-2" placeholder="Nombre" required />
        <input
          v-model="newUser.email"
          class="form-control mb-2"
          type="email"
          placeholder="Email"
          required
        />
        <input
          v-model="newUser.password"
          class="form-control mb-2"
          type="password"
          placeholder="Contraseña"
          required
        />
        <select v-model="newUser.role" class="form-select mb-3">
          <option value="admin">Admin</option>
          <option value="client">Cliente</option>
          <option value="restaurant">Restaurante</option>
        </select>
        <button type="submit" class="btn btn-primary">Crear</button>
      </form>
    </div>

    <!-- Users Table -->
    <table v-if="users.length > 0" class="table table-bordered table-striped">
      <thead class="table-light">
        <tr>
          <th>Nombre</th>
          <th>Email</th>
          <th>Rol</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>
            <button @click="openEditModal(user)" class="btn btn-sm btn-warning me-2">Editar</button>
            <button @click="confirmDelete(user.id)" class="btn btn-sm btn-danger">Borrar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirmar Eliminación</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
          </div>
          <div class="modal-body">¿Estás seguro que deseas eliminar este usuario?</div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancelar
            </button>
            <button type="button" class="btn btn-danger" @click="handleDeleteUser">Eliminar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div class="modal fade" id="editModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <form @submit.prevent="handleEditUser">
            <div class="modal-header">
              <h5 class="modal-title">Editar Usuario</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
            </div>
            <div class="modal-body">
              <input v-model="editUser.name" class="form-control mb-2" placeholder="Nombre" />
              <input
                v-model="editUser.email"
                type="email"
                class="form-control mb-2"
                placeholder="Email"
              />
              <select v-model="editUser.role" class="form-select mb-2">
                <option value="admin">Admin</option>
                <option value="client">Cliente</option>
                <option value="restaurant">Restaurante</option>
              </select>
              <input
                v-model="editUser.password"
                class="form-control"
                type="password"
                placeholder="Nueva contraseña (opcional)"
              />
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                Cancelar
              </button>
              <button type="submit" class="btn btn-primary">Guardar cambios</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'
import { storeToRefs } from 'pinia'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js'

const adminStore = useAdminStore()
const { users, loading, error } = storeToRefs(adminStore)

const newUser = ref({ name: '', email: '', password: '', role: 'client' })
const showAddUserForm = ref(false)
const alert = ref({ message: '', type: '' })

const deleteUserId = ref(null)
const editUser = ref({})

onMounted(() => {
  adminStore.loadUsers()
})

const showAlert = (message, type = 'success') => {
  alert.value = { message, type }
  setTimeout(() => (alert.value = { message: '', type: '' }), 3000)
}

const handleAddUser = async () => {
  try {
    await adminStore.addUser(newUser.value)
    showAlert('Usuario creado correctamente.')
    newUser.value = { name: '', email: '', password: '', role: 'client' }
    showAddUserForm.value = false
  } catch {
    showAlert('Error al crear el usuario.', 'danger')
  }
}

const confirmDelete = (id) => {
  deleteUserId.value = id
  // eslint-disable-next-line no-undef
  new bootstrap.Modal(document.getElementById('deleteModal')).show()
}

const handleDeleteUser = async () => {
  try {
    await adminStore.removeUser(deleteUserId.value)
    showAlert('Usuario eliminado.')
    // eslint-disable-next-line no-undef
    bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide()
  } catch {
    showAlert('Error al eliminar el usuario.', 'danger')
  }
}

const openEditModal = (user) => {
  editUser.value = { ...user }
  // eslint-disable-next-line no-undef
  new bootstrap.Modal(document.getElementById('editModal')).show()
}

const handleEditUser = async () => {
  try {
    const payload = { ...editUser.value }
    if (!payload.password) delete payload.password
    await adminStore.editUser(payload.id, payload)
    showAlert('Usuario actualizado.')
    // eslint-disable-next-line no-undef
    bootstrap.Modal.getInstance(document.getElementById('editModal')).hide()
  } catch {
    showAlert('Error al actualizar usuario.', 'danger')
  }
}
</script>

<style scoped>
.user-management {
  max-width: 900px;
  margin: 0 auto;
}
</style>

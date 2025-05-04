<template>
  <div class="container py-5">
    <h2 class="mb-4">Gestión de Restaurante</h2>

    <div v-if="isLoading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
      <p class="mt-2">Cargando información del restaurante...</p>
    </div>

    <div v-else>
      <div v-if="!restaurant && !isCreatingRestaurant" class="card mb-4">
        <div class="card-header bg-primary text-white">
          <h4 class="mb-0">Registrar Nuevo Restaurante</h4>
        </div>
        <div class="card-body">
          <form @submit.prevent="createRestaurant">
            <div v-if="restaurantError" class="alert alert-danger">{{ restaurantError }}</div>
            <div class="mb-3">
              <label for="restaurantName" class="form-label">Nombre del Restaurante</label>
              <input
                type="text"
                class="form-control"
                id="restaurantName"
                v-model="newRestaurant.name"
                required
              />
            </div>
            <div class="mb-3">
              <label for="restaurantAddress" class="form-label">Dirección</label>
              <input
                type="text"
                class="form-control"
                id="restaurantAddress"
                v-model="newRestaurant.address"
                required
              />
            </div>
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="restaurantPhone" class="form-label">Teléfono</label>
                <input
                  type="tel"
                  class="form-control"
                  id="restaurantPhone"
                  v-model="newRestaurant.phone"
                  required
                />
              </div>
              <div class="col-md-6">
                <label for="restaurantEmail" class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  id="restaurantEmail"
                  v-model="newRestaurant.email"
                  required
                />
              </div>
            </div>
            <div class="mb-3">
              <label for="restaurantDescription" class="form-label">Descripción</label>
              <textarea
                class="form-control"
                id="restaurantDescription"
                v-model="newRestaurant.description"
                rows="3"
                required
              ></textarea>
            </div>
            <div class="mb-3">
              <label for="embeddedMap" class="form-label"
                >Mapa Embebido (código HTML de Google Maps)</label
              >
              <textarea
                class="form-control"
                id="embeddedMap"
                v-model="newRestaurant.embedded_map"
                rows="3"
              ></textarea>
              <small class="text-muted"
                >Opcional: Añade el código iframe de Google Maps para mostrar la ubicación.</small
              >
            </div>
            <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
              <span
                v-if="isSubmitting"
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
              {{ isSubmitting ? 'Registrando...' : 'Registrar Restaurante' }}
            </button>
          </form>
        </div>
      </div>

      <div v-else-if="restaurant">
        <div class="card mb-4">
          <div
            class="card-header bg-primary text-white d-flex justify-content-between align-items-center"
          >
            <h4 class="mb-0">{{ restaurant.name }}</h4>
            <button
              class="btn btn-light btn-sm"
              @click="startRestaurantEdit"
              v-if="!showEditRestaurant"
            >
              <i class="bi bi-pencil-square"></i> Editar Restaurante
            </button>
          </div>
          <div class="card-body">
            <form
              v-if="showEditRestaurant"
              @submit.prevent="submitRestaurantUpdate"
              class="mb-4 p-3 border rounded bg-light"
            >
              <h5>Editando Restaurante</h5>
              <div v-if="restaurantUpdateError" class="alert alert-danger">
                {{ restaurantUpdateError }}
              </div>

              <div class="row">
                <div class="col-md-6 mb-2">
                  <label class="form-label small">Nombre</label>
                  <input
                    v-model="editingRestaurant.name"
                    class="form-control form-control-sm"
                    required
                  />
                </div>
                <div class="col-md-6 mb-2">
                  <label class="form-label small">Dirección</label>
                  <input
                    v-model="editingRestaurant.address"
                    class="form-control form-control-sm"
                    required
                  />
                </div>
                <div class="col-md-6 mb-2">
                  <label class="form-label small">Teléfono</label>
                  <input
                    v-model="editingRestaurant.phone"
                    class="form-control form-control-sm"
                    required
                  />
                </div>
                <div class="col-md-6 mb-2">
                  <label class="form-label small">Email</label>
                  <input
                    v-model="editingRestaurant.email"
                    class="form-control form-control-sm"
                    type="email"
                    required
                  />
                </div>
                <div class="col-12 mb-2">
                  <label class="form-label small">Descripción</label>
                  <textarea
                    v-model="editingRestaurant.description"
                    class="form-control form-control-sm"
                    rows="2"
                    required
                  ></textarea>
                </div>
                <div class="col-12 mb-2">
                  <label class="form-label small">Mapa Embebido (HTML)</label>
                  <textarea
                    v-model="editingRestaurant.embedded_map"
                    class="form-control form-control-sm"
                    rows="2"
                    placeholder="Mapa embebido (opcional)"
                  ></textarea>
                </div>
              </div>
              <button type="submit" class="btn btn-success btn-sm me-2" :disabled="isSubmitting">
                <span
                  v-if="isSubmitting"
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                ></span>
                Guardar Cambios
              </button>
              <button
                type="button"
                class="btn btn-secondary btn-sm"
                @click="cancelRestaurantEdit"
                :disabled="isSubmitting"
              >
                Cancelar
              </button>
            </form>

            <div v-if="!showEditRestaurant" class="row">
              <div class="col-md-6">
                <p><strong>Dirección:</strong> {{ restaurant.address }}</p>
                <p><strong>Teléfono:</strong> {{ restaurant.phone }}</p>
                <p><strong>Email:</strong> {{ restaurant.email }}</p>
                <p><strong>Descripción:</strong> {{ restaurant.description }}</p>
              </div>
              <div class="col-md-6">
                <h5>Ubicación</h5>
                <iframe
                  v-if="restaurant.embedded_map"
                  :src="restaurant.embedded_map"
                  height="450"
                  style="border: 0"
                  allowfullscreen
                  loading="lazy"
                  referrerpolicy="no-referrer-when-downgrade"
                ></iframe>
                <p v-else class="text-muted">Mapa no proporcionado.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="card mb-4">
          <div class="card-header bg-success text-white">
            <h4 class="mb-0">Menú</h4>
          </div>
          <div class="card-body">
            <div v-if="menuItems.length > 0" class="mb-4">
              <h5>Platos Actuales</h5>
              <div class="table-responsive">
                <table class="table table-striped align-middle">
                  <thead>
                    <tr>
                      <th>Nombre</th>
                      <th>Descripción</th>
                      <th>Precio</th>
                      <th>Disponible</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in menuItems" :key="item.id">
                      <td>{{ item.name }}</td>
                      <td>{{ item.description }}</td>
                      <td>€{{ item.price?.toFixed(2) }}</td>
                      <td>
                        <span
                          :class="item.is_available ? 'badge bg-success' : 'badge bg-secondary'"
                        >
                          {{ item.is_available ? 'Sí' : 'No' }}
                        </span>
                      </td>
                      <td>
                        <button
                          class="btn btn-sm btn-primary me-1"
                          @click="startEditMenuItem(item)"
                        >
                          <i class="bi bi-pencil"></i> Editar
                        </button>
                        <button
                          class="btn btn-sm btn-danger"
                          @click="deleteMenuItem(item.id)"
                          :disabled="isSubmitting"
                        >
                          <i class="bi bi-trash"></i> Eliminar
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div v-else class="alert alert-info">
              No tienes platos registrados. Agrega tu primer plato al menú.
            </div>

            <h5 class="mt-4">{{ editingMenuItem ? 'Editar Plato' : 'Agregar Nuevo Plato' }}</h5>
            <div v-if="menuItemError" class="alert alert-danger">{{ menuItemError }}</div>
            <form @submit.prevent="submitMenuItem">
              <div class="row align-items-end">
                <div class="col-md-4 mb-3">
                  <label for="menuItemName" class="form-label">Nombre</label>
                  <input
                    type="text"
                    class="form-control"
                    id="menuItemName"
                    v-model="menuItemForm.name"
                    required
                  />
                </div>
                <div class="col-md-3 mb-3">
                  <label for="menuItemPrice" class="form-label">Precio</label>
                  <div class="input-group">
                    <span class="input-group-text">€</span>
                    <input
                      type="number"
                      class="form-control"
                      id="menuItemPrice"
                      v-model="menuItemForm.price"
                      step="0.01"
                      min="0"
                      required
                    />
                  </div>
                </div>
                <div class="col-md-5 mb-3">
                  <label for="menuItemDescription" class="form-label">Descripción</label>
                  <input
                    type="text"
                    class="form-control"
                    id="menuItemDescription"
                    v-model="menuItemForm.description"
                    required
                  />
                </div>
                <div class="col-md-12 mb-3">
                  <div class="form-check">
                    <input
                      type="checkbox"
                      class="form-check-input"
                      id="menuItemAvailable"
                      v-model="menuItemForm.is_available"
                    />
                    <label class="form-check-label" for="menuItemAvailable">Disponible</label>
                  </div>
                </div>
              </div>
              <button type="submit" class="btn btn-success me-2" :disabled="isSubmitting">
                <span
                  v-if="
                    isSubmitting &&
                    submittingAction === (editingMenuItem ? 'update-menu' : 'add-menu')
                  "
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                ></span>
                {{ editingMenuItem ? 'Guardar Cambios' : 'Agregar al Menú' }}
              </button>
              <button
                type="button"
                class="btn btn-secondary"
                v-if="editingMenuItem"
                @click="cancelEditMenuItem"
                :disabled="isSubmitting"
              >
                Cancelar Edición
              </button>
            </form>
          </div>
        </div>

        <div class="card mb-4">
          <div class="card-header bg-warning text-dark">
            <h4 class="mb-0">Promociones y Descuentos</h4>
          </div>
          <div class="card-body">
            <div v-if="discounts.length > 0" class="mb-4">
              <h5>Promociones Actuales</h5>
              <div class="row">
                <div v-for="discount in discounts" :key="discount.id" class="col-md-4 mb-3">
                  <div class="card h-100">
                    <div class="card-body">
                      <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="card-title mb-0">{{ discount.title }}</h5>
                        <span class="badge bg-danger">{{ discount.percentage }}% OFF</span>
                      </div>
                      <p class="card-text">{{ discount.description }}</p>
                      <p class="card-text mb-0">
                        <small class="text-muted">
                          Válido: {{ formatDate(discount.valid_from) }} -
                          {{ formatDate(discount.valid_until) }}
                        </small>
                      </p>
                    </div>
                    <div class="card-footer bg-transparent border-top-0">
                      <button
                        class="btn btn-sm btn-primary me-1"
                        @click="startEditDiscount(discount)"
                      >
                        <i class="bi bi-pencil"></i> Editar
                      </button>
                      <button
                        class="btn btn-sm btn-danger"
                        @click="deleteDiscount(discount.id)"
                        :disabled="isSubmitting"
                      >
                        <i class="bi bi-trash"></i> Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="alert alert-info">
              No tienes promociones registradas. Agrega tu primera promoción.
            </div>

            <h5 class="mt-4">
              {{ editingDiscount ? 'Editar Promoción' : 'Agregar Nueva Promoción' }}
            </h5>
            <div v-if="discountError" class="alert alert-danger">{{ discountError }}</div>
            <form @submit.prevent="submitDiscount">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="discountTitle" class="form-label">Título</label>
                  <input
                    type="text"
                    class="form-control"
                    id="discountTitle"
                    v-model="discountForm.title"
                    required
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="discountPercentage" class="form-label">Porcentaje de Descuento</label>
                  <div class="input-group">
                    <input
                      type="number"
                      class="form-control"
                      id="discountPercentage"
                      v-model="discountForm.percentage"
                      min="1"
                      max="100"
                      required
                    />
                    <span class="input-group-text">%</span>
                  </div>
                </div>
              </div>
              <div class="mb-3">
                <label for="discountDescription" class="form-label">Descripción</label>
                <textarea
                  class="form-control"
                  id="discountDescription"
                  v-model="discountForm.description"
                  rows="2"
                  required
                ></textarea>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="discountValidFrom" class="form-label">Válido Desde</label>
                  <input
                    type="date"
                    class="form-control"
                    id="discountValidFrom"
                    v-model="discountForm.valid_from"
                    required
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="discountValidUntil" class="form-label">Válido Hasta</label>
                  <input
                    type="date"
                    class="form-control"
                    id="discountValidUntil"
                    v-model="discountForm.valid_until"
                    required
                  />
                </div>
              </div>
              <button type="submit" class="btn btn-warning me-2" :disabled="isSubmitting">
                <span
                  v-if="
                    isSubmitting &&
                    submittingAction === (editingDiscount ? 'update-discount' : 'add-discount')
                  "
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                ></span>
                {{ editingDiscount ? 'Guardar Cambios' : 'Agregar Promoción' }}
              </button>
              <button
                type="button"
                class="btn btn-secondary"
                v-if="editingDiscount"
                @click="cancelEditDiscount"
                :disabled="isSubmitting"
              >
                Cancelar Edición
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import {
  getRestaurantByUserId,
  createRestaurant as createRestaurantService,
  updateRestaurant as updateRestaurantService,
} from '@/services/restaurantService'
import {
  fetchMenuByRestaurantId,
  createMenuItem,
  updateMenuItem as updateMenuItemService,
  deleteMenuItem as deleteMenuItemService,
} from '@/services/menuService'
import {
  fetchDiscountsByRestaurantId,
  createDiscount,
  updateDiscount as updateDiscountService,
  deleteDiscount as deleteDiscountService,
} from '@/services/discountService'

const authStore = useAuthStore()
const router = useRouter()

const user = computed(() => authStore.user)

// State variables
const restaurant = ref(null)
const menuItems = ref([])
const discounts = ref([])

const isLoading = ref(true)
const isSubmitting = ref(false)
const submittingAction = ref('')

const restaurantError = ref('')
const restaurantUpdateError = ref('')
const menuItemError = ref('')
const discountError = ref('')

// Restaurant Edit State
const showEditRestaurant = ref(false)
const editingRestaurant = ref(null)

// Menu Item Edit State and Form Model
const editingMenuItem = ref(null)
const menuItemForm = ref({
  // Single form model for add/edit
  name: '',
  description: '',
  price: null,
  is_available: true,
})

// Discount Edit State and Form Model
const editingDiscount = ref(null)
const discountForm = ref({
  title: '',
  description: '',
  percentage: null,
  valid_from: '',
  valid_until: '',
})

// Restaurant Creation Form Model
const newRestaurant = ref({
  name: '',
  address: '',
  phone: '',
  email: '',
  description: '',
  embedded_map: '',
})
const isCreatingRestaurant = ref(false)

// Fetch all necessary data
const loadRestaurantData = async () => {
  isLoading.value = true
  try {
    if (!user.value || !user.value.id) {
      console.error('User information not available for loading data.')

      isLoading.value = false
      return
    }

    const fetchedRestaurant = await getRestaurantByUserId(user.value.id)
    restaurant.value = fetchedRestaurant

    if (restaurant.value) {
      const [fetchedMenu, fetchedDiscounts] = await Promise.all([
        fetchMenuByRestaurantId(restaurant.value.id),
        fetchDiscountsByRestaurantId(restaurant.value.id),
      ])
      menuItems.value = fetchedMenu
      discounts.value = fetchedDiscounts

      cancelRestaurantEdit()
      cancelEditMenuItem()
      cancelEditDiscount()
    } else {
      menuItems.value = []
      discounts.value = []
    }
  } catch (err) {
    console.error('Error loading restaurant data:', err)
    restaurantError.value = 'Error al cargar los datos del restaurante. Inténtalo de nuevo.'
  } finally {
    isLoading.value = false
  }
}

const createRestaurant = async () => {
  if (!user.value || !user.value.id) {
    restaurantError.value = 'Error: Usuario no identificado.'
    return
  }
  if (isSubmitting.value) return

  isSubmitting.value = true
  isCreatingRestaurant.value = true
  submittingAction.value = 'create-restaurant'
  restaurantError.value = ''

  try {
    const created = await createRestaurantService({
      ...newRestaurant.value,
      user_id: user.value.id,
    })
    restaurant.value = created
    newRestaurant.value = {
      name: '',
      address: '',
      phone: '',
      email: '',
      description: '',
      embedded_map: '',
    }
    await loadRestaurantData()
  } catch (err) {
    console.error('Error creando restaurante:', err)
    restaurantError.value = `Error al registrar: ${err.message || 'Inténtalo de nuevo.'}`
  } finally {
    isSubmitting.value = false
    isCreatingRestaurant.value = false
    submittingAction.value = ''
  }
}

const startRestaurantEdit = () => {
  if (!restaurant.value) return
  editingRestaurant.value = JSON.parse(JSON.stringify(restaurant.value))
  restaurantUpdateError.value = ''
  showEditRestaurant.value = true
}

const cancelRestaurantEdit = () => {
  editingRestaurant.value = null
  showEditRestaurant.value = false
  restaurantUpdateError.value = ''
}

const submitRestaurantUpdate = async () => {
  if (!editingRestaurant.value || !restaurant.value || isSubmitting.value) return

  isSubmitting.value = true
  submittingAction.value = 'update-restaurant'
  restaurantUpdateError.value = ''

  try {
    const updatedData = await updateRestaurantService(restaurant.value.id, editingRestaurant.value)
    restaurant.value = updatedData
  } catch (err) {
    console.error('Error actualizando restaurante:', err)
    restaurantUpdateError.value = `Error al guardar: ${err.message || 'Inténtalo de nuevo.'}`
  } finally {
    isSubmitting.value = false
    submittingAction.value = ''
  }
}

const resetMenuItemForm = () => {
  menuItemForm.value = { name: '', description: '', price: null, is_available: true }
  editingMenuItem.value = null
  menuItemError.value = ''
}

const startEditMenuItem = (item) => {
  menuItemForm.value = JSON.parse(JSON.stringify(item))
  editingMenuItem.value = item
  menuItemError.value = ''
}

const cancelEditMenuItem = () => {
  resetMenuItemForm()
}

const submitMenuItem = async () => {
  if (!restaurant.value || isSubmitting.value) return

  isSubmitting.value = true
  menuItemError.value = ''
  const isEditing = !!editingMenuItem.value
  submittingAction.value = isEditing ? 'update-menu' : 'add-menu'

  try {
    const payload = {
      ...menuItemForm.value,
      restaurant_id: restaurant.value.id,
      price: parseFloat(menuItemForm.value.price) || 0,
      is_available: menuItemForm.value.is_available,
    }

    if (isEditing) {
      const updatedItem = await updateMenuItemService(editingMenuItem.value.id, payload)
      const index = menuItems.value.findIndex((item) => item.id === updatedItem.id)
      if (index !== -1) {
        menuItems.value[index] = updatedItem
      }
    } else {
      const newItem = await createMenuItem(payload, restaurant.value.id)
      menuItems.value.push(newItem)
    }
    resetMenuItemForm()
  } catch (err) {
    console.error(`Error ${isEditing ? 'actualizando' : 'agregando'} plato:`, err)
    menuItemError.value = `Error al guardar: ${err.message || 'Inténtalo de nuevo.'}`
  } finally {
    isSubmitting.value = false
    submittingAction.value = ''
  }
}

const deleteMenuItem = async (itemId) => {
  if (isSubmitting.value) return
  // eslint-disable-next-line no-undef
  if (!confirm('¿Estás seguro de que deseas eliminar este plato del menú?')) {
    return
  }

  isSubmitting.value = true
  submittingAction.value = 'delete-menu'
  menuItemError.value = ''

  try {
    await deleteMenuItemService(itemId)
    menuItems.value = menuItems.value.filter((item) => item.id !== itemId)
  } catch (err) {
    console.error('Error eliminando elemento del menú:', err)
    menuItemError.value = `Error al eliminar: ${err.message || 'Inténtalo de nuevo.'}`
  } finally {
    isSubmitting.value = false
    submittingAction.value = ''
  }
}

const resetDiscountForm = () => {
  discountForm.value = {
    title: '',
    description: '',
    percentage: null,
    valid_from: '',
    valid_until: '',
  }
  editingDiscount.value = null
  discountError.value = ''
}

const startEditDiscount = (discount) => {
  const discountCopy = JSON.parse(JSON.stringify(discount))
  discountCopy.valid_from = discountCopy.valid_from ? discountCopy.valid_from.substring(0, 10) : ''
  discountCopy.valid_until = discountCopy.valid_until
    ? discountCopy.valid_until.substring(0, 10)
    : ''
  discountForm.value = discountCopy
  editingDiscount.value = discount
  discountError.value = ''
}

const cancelEditDiscount = () => {
  resetDiscountForm()
}

const submitDiscount = async () => {
  if (!restaurant.value || isSubmitting.value) return

  isSubmitting.value = true
  discountError.value = ''
  const isEditing = !!editingDiscount.value
  submittingAction.value = isEditing ? 'update-discount' : 'add-discount'

  if (
    discountForm.value.valid_from &&
    discountForm.value.valid_until &&
    discountForm.value.valid_from > discountForm.value.valid_until
  ) {
    discountError.value = 'La fecha "Válido Desde" no puede ser posterior a "Válido Hasta".'
    isSubmitting.value = false
    submittingAction.value = ''
    return
  }

  try {
    const payload = {
      ...discountForm.value,
      restaurant_id: restaurant.value.id,
      percentage: parseInt(discountForm.value.percentage) || 0,
    }

    if (isEditing) {
      const updatedDiscount = await updateDiscountService(editingDiscount.value.id, payload)
      const index = discounts.value.findIndex((d) => d.id === updatedDiscount.id)
      if (index !== -1) {
        discounts.value[index] = updatedDiscount
      }
    } else {
      const newDiscount = await createDiscount(payload)
      discounts.value.push(newDiscount)
    }
    resetDiscountForm()
  } catch (err) {
    console.error(`Error ${isEditing ? 'actualizando' : 'agregando'} promoción:`, err)
    discountError.value = `Error al guardar: ${err.message || 'Inténtalo de nuevo.'}`
  } finally {
    isSubmitting.value = false
    submittingAction.value = ''
  }
}

const deleteDiscount = async (discountId) => {
  if (isSubmitting.value) return
  // eslint-disable-next-line no-undef
  if (!confirm('¿Estás seguro de que deseas eliminar esta promoción?')) {
    return
  }

  isSubmitting.value = true
  submittingAction.value = 'delete-discount'
  discountError.value = ''

  try {
    await deleteDiscountService(discountId)
    discounts.value = discounts.value.filter((d) => d.id !== discountId)
  } catch (err) {
    console.error('Error eliminando promoción:', err)
    discountError.value = `Error al eliminar: ${err.message || 'Inténtalo de nuevo.'}`
  } finally {
    isSubmitting.value = false
    submittingAction.value = ''
  }
}

// ---- Utility Functions ----
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) {
      return dateString
    }
    return date.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    })
  } catch (e) {
    console.error('Error formatting date:', e, dateString)
    return dateString
  }
}

// --- Lifecycle Hooks ---
onMounted(async () => {
  if (!authStore.isAuthenticated || !user.value) {
    router.push('/login')
    return
  }
  await loadRestaurantData()
})

watch(
  user,
  async (newUser, oldUser) => {
    if (newUser?.id !== oldUser?.id) {
      console.log('User changed, reloading restaurant data...')
      await loadRestaurantData()
    }
  },
  { deep: true },
)
</script>

<style scoped>
.card-header {
  font-weight: 500;
}

.form-label.small {
  margin-bottom: 0.2rem;
  font-size: 0.8em;
  font-weight: 500;
}

.table {
  table-layout: fixed;
  word-wrap: break-word;
}

.table th,
.table td {
  vertical-align: middle;
}

.btn .spinner-border-sm {
  margin-right: 0.5em;
}
</style>

<template>
  <BaseLayout>
    <div class="auth-page container py-5">
      <h1 class="mb-4 text-center">Sign Up</h1>

      <form
        @submit.prevent="handleSignup"
        class="auth-form card p-4 shadow-sm mx-auto"
        style="max-width: 400px"
      >
        <!-- Name Input -->
        <div class="mb-3">
          <label class="form-label">Name</label>
          <input v-model="name" type="text" class="form-control" required />
        </div>

        <!-- Email Input -->
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="email" type="email" class="form-control" required />
        </div>

        <!-- Password Input -->
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" required minlength="6" />
        </div>

        <!-- Role Selector (Usuario or Restaurante) -->
        <div class="mb-3">
          <label class="form-label">Role</label>
          <select v-model="role" class="form-control" required>
            <option value="" disabled selected>Selecciona tu rol</option>
            <!-- Loop through roles and create an option for each -->
            <option v-for="role in roles" :key="role" :value="role">
              {{ role.name }}
            </option>
          </select>
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-success w-100" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          Sign Up
        </button>

        <!-- Error Message -->
        <div v-if="error" class="alert alert-danger mt-3">
          {{ error }}
        </div>

        <!-- Link to Login -->
        <div class="text-center mt-3">
          <RouterLink to="/login">¿Ya tienes una cuenta? Accede</RouterLink>
        </div>
      </form>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { signup } from '@/services/authService'
import { fetchStandardRoles } from '@/services/roleService'
import BaseLayout from '@/views/layouts/BaseLayout.vue'

const name = ref('')
const email = ref('')
const password = ref('')
const role = ref('')
const loading = ref(false)
const error = ref(null)
const roles = ref([]) //

const router = useRouter()

const fetchRoles = async () => {
  loading.value = true
  try {
    const data = await fetchStandardRoles()
    roles.value = data
  } catch (err) {
    console.error('Error fetching roles:', err)
    error.value = 'Failed to load available roles'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRoles()
})

const handleSignup = async () => {
  loading.value = true
  error.value = null
  try {
    await signup({
      name: name.value,
      email: email.value,
      password: password.value,
      role: role.value.name,
    })
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.message || 'Signup failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

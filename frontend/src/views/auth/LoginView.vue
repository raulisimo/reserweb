<template>
  <BaseLayout>
    <div class="auth-page container py-5">
      <h1 class="mb-4 text-center">Login</h1>

      <form
        @submit.prevent="handleLogin"
        class="auth-form card p-4 shadow-sm mx-auto"
        style="max-width: 400px"
      >
        <!-- Email input field -->
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="email" type="email" class="form-control" required />
        </div>

        <!-- Password input field -->
        <div class="mb-3">
          <label class="form-label">Contraseña</label>
          <input v-model="password" type="password" class="form-control" required />
        </div>

        <!-- Submit button -->
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          Login
        </button>

        <!-- Error message if login fails -->
        <div v-if="error" class="alert alert-danger mt-3">
          {{ error }}
        </div>

        <!-- Link to Signup page -->
        <div class="text-center mt-3">
          <RouterLink to="/signup">¿No tienes una cuenta? Registrate</RouterLink>
        </div>
      </form>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseLayout from '@/views/layouts/BaseLayout.vue'

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

const router = useRouter()
const authStore = useAuthStore()

// Handle the login process
const handleLogin = async () => {
  loading.value = true
  error.value = null

  try {
    // Use the auth store to perform login
    await authStore.login({ email: email.value, password: password.value })

    // Redirect to home after successful login
    router.push('/')
  } catch (err) {
    console.error('Login failed:', err)

    // Handle error, show appropriate message
    error.value = err?.response?.data?.message || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-form {
  max-width: 400px;
}

.spinner-border {
  margin-right: 8px;
}

.alert {
  font-size: 14px;
  margin-top: 15px;
}

.text-center {
  margin-top: 20px;
}
</style>

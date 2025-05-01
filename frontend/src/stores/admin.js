import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getUsers, createUser, updateUser, deleteUser } from '@/services/adminService'

export const useAdminStore = defineStore('admin', () => {
  const users = ref([])
  const loading = ref(false)
  const error = ref(null)

  const loadUsers = async () => {
    loading.value = true
    error.value = null
    try {
      users.value = await getUsers()
    } catch (err) {
      error.value = err.message || 'Error loading users.'
      console.error('[AdminStore] loadUsers:', err)
    } finally {
      loading.value = false
    }
  }

  const addUser = async (userData) => {
    try {
      const newUser = await createUser(userData)
      users.value.push(newUser)
    } catch (err) {
      error.value = err.message || 'Error creating user.'
      console.error('[AdminStore] addUser:', err)
      throw err
    }
  }

  const editUser = async (userId, userData) => {
    try {
      const updatedUser = await updateUser(userId, userData)
      const index = users.value.findIndex((u) => u.id === userId)
      if (index !== -1) users.value[index] = updatedUser
    } catch (err) {
      error.value = err.message || 'Error updating user.'
      console.error('[AdminStore] editUser:', err)
      throw err
    }
  }

  const removeUser = async (userId) => {
    try {
      await deleteUser(userId)
      users.value = users.value.filter((u) => u.id !== userId)
    } catch (err) {
      error.value = err.message || 'Error deleting user.'
      console.error('[AdminStore] removeUser:', err)
      throw err
    }
  }

  return {
    users,
    loading,
    error,
    loadUsers,
    addUser,
    editUser,
    removeUser,
  }
})

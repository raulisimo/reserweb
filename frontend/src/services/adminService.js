import { apiUrl } from '@/config'
import { getAuthHeaders } from '@/services/utils'

export const getUsers = async () => {
  const response = await fetch(`${apiUrl}/users/all`, {
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch users: ${response.statusText}`)
  }

  return await response.json()
}

export const createUser = async (userData) => {
  const response = await fetch(`${apiUrl}/users/create`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(userData),
  })

  if (!response.ok) {
    throw new Error(`Failed to create user: ${response.statusText}`)
  }

  return await response.json()
}

export const updateUser = async (userId, userData) => {
  const response = await fetch(`${apiUrl}/users/${userId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(userData),
  })

  if (!response.ok) {
    throw new Error(`Failed to update user: ${response.statusText}`)
  }

  return await response.json()
}

export const deleteUser = async (userId) => {
  const response = await fetch(`${apiUrl}/users/${userId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    throw new Error(`Failed to delete user: ${response.statusText}`)
  }
  return await response.json()
}

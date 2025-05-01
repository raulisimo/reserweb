import { apiUrl } from '@/config'
import { getAuthHeaders } from '@/services/utils'

export async function fetchRestaurants() {
  try {
    const response = await fetch(`${apiUrl}/restaurants`)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Failed to fetch restaurants:', error)
    throw error
  }
}

export async function fetchRestaurantswithScore() {
  try {
    const response = await fetch(`${apiUrl}/restaurants/with-scores`)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Failed to fetch restaurants:', error)
    throw error
  }
}

export async function searchRestaurants(query) {
  try {
    const response = await fetch(`${apiUrl}/restaurants/search?query=${query}`)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Failed to fetch restaurants:', error)
    throw error
  }
}

export async function fetchRestaurantDetails(restaurantId) {
  try {
    const response = await fetch(`${apiUrl}/restaurants/${restaurantId}`)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }
    const data = await response.json()

    return data
  } catch (error) {
    console.error('Failed to fetch restaurant details:', error)
    throw error
  }
}

export async function getRestaurantByUserId(userId) {
  const response = await fetch(`${apiUrl}/restaurants/user/${userId}`)
  if (!response.ok) throw new Error('Failed to fetch restaurant')
  return await response.json()
}

export const createRestaurant = async (data) => {
  const res = await fetch(`${apiUrl}/restaurants`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Error creating restaurant')
  return res.json()
}

export const updateRestaurant = async (id, data) => {
  const res = await fetch(`${apiUrl}/restaurants/${id}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Error updating restaurant')
  return res.json()
}

export const deleteRestaurant = async (id) => {
  const res = await fetch(`${apiUrl}/restaurants/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  })
  if (!res.ok) throw new Error('Error deleting restaurant')
  return res.status === 204 ? true : res.json()
}

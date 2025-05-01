import { apiUrl } from '@/config'
import { getAuthHeaders } from './utils'

export const fetchMenuByRestaurantId = async (restaurantId) => {
  const res = await fetch(`${apiUrl}/restaurants/${restaurantId}/menu`, {
    headers: getAuthHeaders(),
  })
  if (!res.ok) throw new Error('Error al obtener el menú')
  return res.json()
}

export const createMenuItem = async (data, restaurantId) => {
  console.log('Creating menu item:', data, restaurantId)
  const res = await fetch(`${apiUrl}/menu/restaurant/${restaurantId}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return await res.json()
}

export const deleteMenuItem = async (itemId) => {
  const res = await fetch(`${apiUrl}/menu/${itemId}`, {
    method: 'DELETE',
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.detail || 'Error deleting menu item')
  }

  return true
}

export const updateMenuItem = async (menuItemId, data) => {
  const res = await fetch(`${apiUrl}/menu/${menuItemId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return await res.json()
}

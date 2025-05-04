import { apiUrl } from '@/config'
import { getAuthHeaders } from './utils'

export const fetchDiscountsByRestaurantId = async (restaurantId) => {
  const res = await fetch(`${apiUrl}/discounts/restaurant/${restaurantId}`, {
    headers: getAuthHeaders(),
  })
  if (!res.ok) throw new Error('Error al obtener los descuentos')
  return res.json()
}

export const createDiscount = async (data) => {
  const res = await fetch(`${apiUrl}/discounts/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return await res.json()
}

export const deleteDiscount = async (discountId) => {
  const res = await fetch(`${apiUrl}/discounts/${discountId}`, {
    method: 'DELETE',
  })

  if (!res.ok) {
    throw new Error('Failed to delete discount')
  }

  return true
}

export const updateDiscount = async (discountId, data) => {
  console.log('Updating discount with ID:', discountId, data)
  const res = await fetch(`${apiUrl}/discounts/${discountId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

  if (!res.ok) {
    throw new Error('Failed to update discount')
  }

  return await res.json()
}

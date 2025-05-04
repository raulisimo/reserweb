import { apiUrl } from '@/config'
import { getAuthHeaders } from '@/services/utils'

export async function fetchReviews() {
  try {
    const response = await fetch(`${apiUrl}/reviews/all`)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Failed to fetch reviews:', error)
    throw error
  }
}

export const fetchResturantReviews = async (id) => {
  const response = await fetch(`${apiUrl}/reviews/restaurant/${id}`, {
    headers: {
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error('Failed to fetch reviews')
  }

  return await response.json()
}

export const createReview = async (data) => {
  const res = await fetch(`${apiUrl}/reviews/create`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Error creating review')
  return res.json()
}

export const updateReview = async (id, data) => {
  console.log('Updating review with ID:', data)
  const res = await fetch(`${apiUrl}/reviews/${id}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  })

  if (!res.ok) throw new Error('Error updating review')
  return res.json()
}

export const deleteReview = async (id) => {
  const res = await fetch(`${apiUrl}/reviews/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  })
  if (!res.ok) throw new Error('Error deleting review')
  return res.status === 204 ? true : res.json()
}

export const fetchUserReviews = async (userId) => {
  const res = await fetch(`${apiUrl}/reviews/user/${userId}`, {
    headers: getAuthHeaders(),
  })
  if (!res.ok) throw new Error('Failed to fetch user reviews')
  return res.json()
}

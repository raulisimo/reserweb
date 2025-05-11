import { apiUrl } from '@/config'

export const createBooking = async (bookingData) => {
  // eslint-disable-next-line no-undef
  const token = localStorage.getItem('access_token')

  const response = await fetch(`${apiUrl}/bookings/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(bookingData),
  })

  if (!response.ok) {
    throw new Error(`Booking failed: ${response.statusText}`)
  }

  const data = await response.json()
  return data
}

export const getBookingsByClient = async () => {
  // eslint-disable-next-line no-undef
  const token = localStorage.getItem('access_token')
  const response = await fetch(`${apiUrl}/bookings/user`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    throw new Error(`Booking retrieval failed: ${response.statusText}`)
  }

  const data = await response.json()
  return data
}

export const getBookingsByRestaurant = async () => {
  // eslint-disable-next-line no-undef
  const token = localStorage.getItem('access_token')

  const response = await fetch(`${apiUrl}/bookings/restaurant/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    throw new Error(`Booking retrieval failed: ${response.statusText}`)
  }

  const data = await response.json()
  console.log('Bookings by restaurant:', data)
  return data
}

export const deleteBookingByUser = async (bookingId) => {
  // eslint-disable-next-line no-undef
  const token = localStorage.getItem('access_token')

  const response = await fetch(`${apiUrl}/bookings/user/${bookingId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    throw new Error(`Booking deletion failed: ${response.statusText}`)
  }

  const data = await response.json()
  return data
}

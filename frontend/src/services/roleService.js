import { apiUrl } from '@/config'

export async function fetchStandardRoles() {
  try {
    const response = await fetch(`${apiUrl}/roles/get-standard-roles`)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Failed to fetch roles:', error)
    throw error
  }
}

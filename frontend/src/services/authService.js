import { apiUrl } from '@/config'

export const login = async (credentials) => {
  const response = await fetch(`${apiUrl}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  })

  if (!response.ok) {
    throw new Error('Login failed: ' + response.statusText)
  }

  const data = await response.json()
  return data
}

export const signup = async (data) => {
  const response = await fetch(`${apiUrl}/auth/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error('Signup failed: ' + response.statusText)
  }

  const result = await response.json()
  return result
}

export const logout = async () => {
  const response = await fetch(`${apiUrl}/auth/logout`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error('Logout failed: ' + response.statusText)
  }

  const result = await response.json()
  return result
}

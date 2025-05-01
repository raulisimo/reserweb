export const getAuthHeaders = () => ({
  'Content-Type': 'application/json',
  // eslint-disable-next-line no-undef
  Authorization: `Bearer ${localStorage.getItem('access_token')}`,
})

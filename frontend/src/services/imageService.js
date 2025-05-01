export async function fetchUnsplashImages(query, perPage = 1, page = 1) {
  const apiKey = import.meta.env.VITE_UNSPLASH_ACCESS_KEY
  const url = `https://api.unsplash.com/search/photos?query=${query}&page=${page}&per_page=${perPage}&client_id=${apiKey}`

  try {
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }

    const data = await response.json()

    if (data.results.length === 0) {
      return []
    }

    return data.results
  } catch (error) {
    console.error('Failed to fetch Unsplash images:', error)
    throw error
  }
}

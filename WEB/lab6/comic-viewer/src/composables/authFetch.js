export async function authFetch(url, options = {}) {
  const token = localStorage.getItem('token')

  // Attach Authorization header
  const headers = {
    ...(options.headers || {}),
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  }

  const response = await fetch(url, {
    ...options,
    headers,
  })

  console.log(response);

  // Redirect to login on 401
  if (response.status === 401 || response.status === 403) {
    localStorage.removeItem('token')
    const { default: router } = await import('../router');
    router.push('/login');
  }

  return response
}
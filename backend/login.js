const username = document.getElementById('username')
const password = document.getElementById('password')
const loginBtn = document.getElementById('login-btn')

loginBtn && loginBtn.addEventListener('click', loginUser)
const response = document.getElementById('response')

console.log('Login script loaded')
function loginUser(event) {
  event.preventDefault()
  const u = username?.value?.trim() ?? ''
  const p = password?.value?.trim() ?? ''
  console.debug('validate:', { u, pLength: p.length }) // added debug

  if (!u) {
    response.textContent = 'No username was found'
    password.value = ''
    return false
  }

  if (!p) {
    response.textContent = 'No password was found'
    return false
  }

  const loginData = { username: u, password: p }
  console.log(loginData)
  response.textContent = 'Inputs valid'

  fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(loginData),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log('Success:', data)
      response.textContent = data.message || 'Login successful'
    })
    .catch((error) => {
      console.error('Error:', error)
      response.textContent = 'An error occurred during login'
    })
}

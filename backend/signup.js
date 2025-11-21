const username = document.getElementById('username')
const email = document.getElementById('email')
const password = document.getElementById('password')
const signupBtn = document.getElementById('signup-btn')
const response = document.getElementById('response')

signupBtn && signupBtn.addEventListener('click', checkUser)

console.log('Script loaded')

function isEmailValid(e) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)
}

function checkUser(event) {
  event.preventDefault()

  const u = username?.value?.trim() ?? ''
  const em = email?.value?.trim() ?? ''
  const pw = password?.value ?? ''

  console.debug('validate:', { u, em, pwLength: pw.length }) // added debug

  if (!u) {
    response.textContent = 'No username was found'
    password.value = ''
    return false
  }
  if (!em) {
    response.textContent = 'No email was found'
    password.value = ''
    return false
  }
  if (!isEmailValid(em)) {
    response.textContent = 'Invalid email format'
    password.value = ''
    return false
  }
  if (!pw) {
    response.textContent = 'No password was found'
    return false
  }
  // allow passwords of length 8 and up
  if (pw.length < 8) {
    response.textContent = 'The password should be 8 characters and up'
    password.value = ''
    return false
  }

  const userData = {
    username: u,
    email: em,
    password: pw,
  }

  console.log(userData)

  response.textContent = 'Inputs valid'

  fetch('http://localhost:8000/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data)
      response.textContent = data.message || 'user created successfully'
      console.log(userData)
    })
    .catch((err) => {
      response.textContent = 'Error sending data to server'
      console.error(err)
    })

  return true
}

const addressBtn = document.querySelector('#moims--index--address')
const addressDiv = document.querySelector('#moims--index--address--block')

const filterBtn = document.querySelector('#moims--index--filter')
const filterDiv = document.querySelector('#moims--index--filter--block')

// 큰 모달 d-block
addressBtn.addEventListener('click', (event) => {
  addressDiv.classList.remove('d-none')
  if (!filterDiv.classList.contains('d-none')) {
    filterDiv.classList.add('d-none')
  }
})


filterBtn.addEventListener('click', (event) => {
  filterDiv.classList.remove('d-none')
  if (!addressDiv.classList.contains('d-none')) {
    addressDiv.classList.add('d-none')
  }
})


// 큰 모달 창 닫기
const addressClose = document.querySelector('#moims--index--address--close')
const filterClose = document.querySelector('#moims--index--filter--close')

addressClose.addEventListener('click', (event) => {
  addressDiv.classList.add('d-none')
})

filterClose.addEventListener('click', (event) => {
  filterDiv.classList.add('d-none')
})

// header search
const postsContainer = document.querySelector('.moims--index--section')
const searchBtn = document.querySelector('#moims--index--search')
const searchForm = document.querySelector('#moims--index--search--block')
const searchInput = document.querySelector('#moims--index--search--block > input[type="search"]')

searchBtn.addEventListener('click', (event) => {
  searchBtn.classList.add('d-none')
  searchForm.classList.remove('d-none')
  if (!addressDiv.classList.contains('d-none')) {
    addressDiv.classList.add('d-none')
  } else if (!filterDiv.classList.contains('d-none')) {
    filterDiv.classList.add('d-none')
  }
  
})

searchInput.addEventListener('input', async (event) => {
  const searchValue = event.target.value
  const urlParams = new URLSearchParams(window.location.search)
  const disValue = urlParams.get('dis')
  const categoryValue = urlParams.get('category')

  try {
    const response = await fetch(
      `/moims/?category=${categoryValue}&dis=${disValue}&q=${searchValue}`
    )
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const html = await response.text()
    const parser = new DOMParser()
    const doc = parser.parseFromString(html, 'text/html')
    const posts = doc.querySelector('.moims--index--section')
 
    if (searchValue) {
      const regex = new RegExp(searchValue, 'gi')
      const h1Elements = posts.querySelectorAll('h1')
      h1Elements.forEach((h1) => {
        const originalContent = h1.innerHTML
        const highlightedContent = originalContent.replace(regex, (match) => `<span class="moims--index--highlight">${match}</span>`)
        h1.innerHTML = highlightedContent
      })
    }
    
    postsContainer.innerHTML = posts.innerHTML
    
    const emptyDiv = document.querySelector('.moims--index--empty')

    if (emptyDiv) {
      emptyDiv.textContent = '일치하는 검색어가 없습니다 😥'
    }

  } catch (error) {
    console.error(error)
  }
})

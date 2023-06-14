const postsContainer = document.querySelector('.communities--index--section')
const sortBtn = document.querySelector('.communities--index--order--btn')
const sortDiv = document.querySelector('.communities--index--order--collapse')

if (sortBtn) {
  sortBtn.addEventListener('click', (event) => {
    if (sortDiv.classList.contains('d-none')) {
      sortDiv.classList.remove('d-none')
    } else {
      sortDiv.classList.add('d-none')
    }
  })
  
  document.addEventListener('click', (event) => {
    const target = event.target
    if (!sortBtn.contains(target) && !sortDiv.contains(target)) {
      sortDiv.classList.add('d-none')
    }
  })
}

// 활동 점수
const boltBtns = document.querySelectorAll('.communities--index--topwriters-item section')

boltBtns.forEach((btn) => {
  const boltCollapse = btn.querySelector('div')

  btn.addEventListener('mouseenter', (event) => {
    boltCollapse.classList.remove('d-none')
  })

  btn.addEventListener('mouseleave', (event) => {
    boltCollapse.classList.add('d-none')
  })
})

// 검색
const searchInput = document.querySelector('.communities--index--create--form input')

searchInput.addEventListener('input', async (event) => {
  const searchValue = event.target.value
  const urlParams = new URLSearchParams(window.location.search)
  const categoryValue = urlParams.get('category')
  const tagValue = urlParams.get('tag')

  try {
    const response = await fetch(
      `/communities/?category=${categoryValue}&tag=${tagValue}&q=${searchValue}`
    )
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const html = await response.text()
    const parser = new DOMParser()
    const doc = parser.parseFromString(html, 'text/html')
    const posts = doc.querySelector('.communities--index--section')

    if (searchValue) {
      const regex = new RegExp(searchValue, 'gi')

      const h1Elements = posts.querySelectorAll('.communities--index--section--item--section')

      h1Elements.forEach((h1) => {
        const originalContent = h1.innerHTML
        const highlightedContent = originalContent.replace(regex, (match) => `<span class="communities--index--highlight">${match}</span>`)
        h1.innerHTML = highlightedContent
      })

      const tagElements = posts.querySelectorAll('.communities--index--section--item--tag')

      tagElements.forEach((tag) => {
        const originalContent = tag.innerHTML
        const highlightedContent = originalContent.replace(regex, (match) => `<span class="communities--index--highlight">${match}</span>`)
        tag.innerHTML = highlightedContent
      })
    }
    
    postsContainer.innerHTML = posts.innerHTML
    
    const emptyDiv = document.querySelector('.communities--index--empty')

    if (emptyDiv) {
      emptyDiv.textContent = '일치하는 검색어가 없습니다 😥'
    }

  } catch (error) {
    console.error(error)
  }
})
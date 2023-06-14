const addressBtn = document.querySelector('#markets--index--address')
const addressDiv = document.querySelector('#markets--index--address--block')

const filterBtn = document.querySelector('#markets--index--filter')
const filterDiv = document.querySelector('#markets--index--filter--block')

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
const addressClose = document.querySelector('#markets--index--address--close')
const filterClose = document.querySelector('#markets--index--filter--close')

addressClose.addEventListener('click', (event) => {
  addressDiv.classList.add('d-none')
})

filterClose.addEventListener('click', (event) => {
  filterDiv.classList.add('d-none')
})

// header search
const postsContainer = document.querySelector('.markets--index--section')
const searchBtn = document.querySelector('#markets--index--search')
const searchForm = document.querySelector('#markets--index--search--block')
const searchInput = document.querySelector('#markets--index--search--block > input[type="search"]')
 
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
      `/markets/?dis=${disValue}&category=${categoryValue}&q=${searchValue}`
    )

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const html = await response.text()
    const parser = new DOMParser()
    const doc = parser.parseFromString(html, 'text/html')
    const posts = doc.querySelector('.markets--index--section')

    if (searchValue) {
      const regex = new RegExp(searchValue, 'gi')
      const h1Elements = posts.querySelectorAll('h1')
      h1Elements.forEach((h1) => {
        const originalContent = h1.innerHTML
        const highlightedContent = originalContent.replace(regex, (match) => `<span class="markets--index--highlight">${match}</span>`)
        h1.innerHTML = highlightedContent
      })
    }

    postsContainer.innerHTML = posts.innerHTML

    const emptyDiv = document.querySelector('.markets--index--empty')

    if (emptyDiv) {
      emptyDiv.textContent = '일치하는 검색어가 없습니다 😥'
    }
  } catch (error) {
    console.error(error)
  }
})


// 마켓 인덱스 좋아요 비동기

const indexLikeForms = document.querySelectorAll('.markets--index--section--likes')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const likeAlert = document.querySelector('#markets--index--alert')
let likeAlertSave

indexLikeForms.forEach((form) => {
  form.addEventListener('submit', function (event) {
    event.preventDefault()
    const postId = event.target.dataset.postId

    axios({
      method: "POST",
      url: `/markets/${postId}/likes/`,
      headers: {'X-CSRFToken': csrftoken},
    })
      .then((response) => {
        if (response.data.error) {
          const errorMessage = response.data.error

          if (likeAlert.style.display == 'none') {
            if (likeAlert.innerHTML.includes('<h1>')) {
              likeAlertSave = likeAlert.innerHTML
            }
            
            likeAlert.innerHTML = errorMessage
            likeAlert.style.display = 'block'
            likeAlert.style.opacity = '1'
    
            setTimeout(() => {
              likeAlert.style.opacity = '0.9'
              setTimeout(() => {
                likeAlert.style.opacity = '0.8'
                setTimeout(() => {
                  likeAlert.style.opacity = '0.7'
                  setTimeout(() => {
                    likeAlert.style.display = 'none'
                  }, 50)
                }, 50)
              }, 50)
            }, 1500)
          }
        } else {
          const isLiked = response.data.is_liked
          const likeBtnIcon = form.querySelector(`#like-${postId} i`)
          const likeCount = form.querySelector(`#like-${postId} span`)

          if (isLiked === true) {
            likeBtnIcon.classList.remove('bi-heart')
            likeBtnIcon.classList.add('bi-heart-fill')
            likeCount.textContent = parseInt(likeCount.textContent) + 1

            if (likeAlert.style.display == 'none') {
              if (typeof likeAlertSave !== 'undefined') {
                likeAlert.innerHTML = likeAlertSave
              }

              likeAlert.style.display = 'flex'
              likeAlert.style.opacity = '1'
              
              setTimeout(() => {
                likeAlert.style.opacity = '0.9'
                setTimeout(() => {
                  likeAlert.style.opacity = '0.8'
                  setTimeout(() => {
                    likeAlert.style.opacity = '0.7'
                    setTimeout(() => {
                      likeAlert.style.display = 'none'
                    }, 50)
                  }, 50)
                }, 50)
              }, 2500)
            }
          } else {
            likeBtnIcon.classList.remove('bi-heart-fill')
            likeBtnIcon.classList.add('bi-heart')
            likeCount.textContent = parseInt(likeCount.textContent) - 1
          }
        }
      })
      .catch((error) => {
        console.log(error.response)
      })
  })
})
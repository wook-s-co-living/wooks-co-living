const carouselDblock = document.querySelector('.markets--carousel--dblock')
const carouselBtns = document.querySelectorAll('.markets--carousel--dblock .item')
const carouselDnone = document.querySelector('.markets--carousel--dnone')
const detailContainer = document.querySelector('.markets--detail--container')
let owlCarousel = $('.owl-carousel')

const detailBody = document.querySelector('.markets--detail')
const detailNavbar = document.querySelector('.markets--detail--navbar')
const navbar = document.querySelector('.nav--bar')
const footer = document.querySelector('.footer')

carouselBtns.forEach((btn) => {
  btn.addEventListener('click', (event) => {
    carouselDblock.classList.add('d-none')
    
    const containerChildren = detailContainer.childNodes
    containerChildren.forEach((element) => {
      if (element !== carouselDnone && element.nodeType === 1) {
        element.classList.add('d-none')
      }
    })
    
    carouselDnone.classList.remove('d-none')
    detailContainer.style = 'max-width: 600px'
    detailBody.style = 'background-color: black'
    
    const btnValue = btn.value
    owlCarousel.trigger('to.owl.carousel', [btnValue - 1])
    navbar.style.display = 'none'
    footer.style.display = 'none'
  })
})


const closeBtn = document.querySelector('.owl--carousel--close')
const carouselDnoneItems = document.querySelectorAll('.markets--carousel--dnone .owl-item')

closeBtn.addEventListener('click', (event) => {
  const containerChildren = detailContainer.childNodes
    containerChildren.forEach((element) => {
      if (element !== carouselDnone && element.nodeType === 1) {
        element.classList.remove('d-none')
      }
    })
  carouselDnone.classList.add('d-none')
  detailContainer.style = ''
  detailBody.style = 'background-color: white'
  
  carouselDnoneItems.forEach((item) => {
    if (item.classList.contains('active')) {
      itemValue = item.querySelector('button').value
    }
  })
  
  owlCarousel.trigger('to.owl.carousel', [itemValue - 1])
  navbar.style.display = 'flex'
  footer.style.display = 'block'
})

// detail info

const infoBtn = document.querySelector('#markets--detail--header--info')
const infoBlock = document.querySelector('.markets--detail--header--infobox')

infoBtn.addEventListener('mouseenter', (event) => {
  infoBlock.classList.remove('d-none')
})

infoBtn.addEventListener('mouseleave', (event) => {
  infoBlock.classList.add('d-none')
})

// detail like form
const likeForm = document.querySelector('#markets--detail--like--form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const likeAlert = document.querySelector('#markets--detail--alert')

likeForm.addEventListener('submit', function (event) {
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
        const likeBtnIcon = likeForm.querySelector('.bi')
        const likeCount = document.querySelector('#markets--detail--section-likecount')

        if (isLiked == true) {
          likeBtnIcon.classList.remove('bi-heart')
          likeBtnIcon.classList.add('bi-heart-fill')
          likeCount.textContent = parseInt(likeCount.textContent) + 1

          if (likeAlert.style.display == 'none') {

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
        } else if (isLiked == false) {
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
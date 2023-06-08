const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

document.addEventListener('DOMContentLoaded', function() {

  document.getElementById('communities--detail--share').addEventListener('click', function() {
      var currentUrl = window.location.href
      var tempInput = document.createElement('input')

      tempInput.value = currentUrl
      document.body.appendChild(tempInput)

      tempInput.select()

      document.execCommand('copy')
 
      document.body.removeChild(tempInput)

      alert('URL이 복사되었습니다!')
  })
})

// 디테일 모달

const detailUpdateBtn = document.querySelector('#communities--detail--update--button')
const detailUpdateModal = document.querySelector('#communities--detail--update--modal')

if(detailUpdateBtn) {
  detailUpdateBtn.addEventListener('click', (event) => {
    if(detailUpdateModal.style.display == 'none') {
      detailUpdateModal.style.display = 'block'
    } else {
      detailUpdateModal.style.display = 'none'
    }
  })
}

document.addEventListener('click', (event) => {
  if (detailUpdateBtn) {
    if (event.target !== detailUpdateBtn && !detailUpdateBtn.contains(event.target)) {
      detailUpdateModal.style.display = 'none'
    }
  }
})

// 디테일 scrape

const scrapeForm = document.querySelector('#communities--detail--scrape')
const likeAlert = document.querySelector('#communities--detail--alert')

if (scrapeForm) {
  scrapeForm.addEventListener('submit', (event) => {
    event.preventDefault()

    const postId = event.target.dataset.postId

    axios({
      method: "POST",
      url: `/communities/${postId}/scrapes/`,
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
          
          const isScrped = response.data.is_scraped
          const scrapeBtnIcon = scrapeForm.querySelector('.bi')

          if (isScrped == true) {
            scrapeBtnIcon.classList.remove('bi-bookmark')
            scrapeBtnIcon.classList.add('bi-bookmark-fill')
            scrapeBtnIcon.style.color = '#34568b'

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
          } else if (isScrped == false) {
            scrapeBtnIcon.classList.remove('bi-bookmark-fill')
            scrapeBtnIcon.classList.add('bi-bookmark')
          }

        }
      })

      .catch((error) => {
        console.log(error.response)
      })
  })
}

// 디테일 post 좋아요 싫어요

const likeForm = document.querySelector('.communities--detail--section--footer form')

if (likeForm) {
  likeForm.addEventListener('submit', (event) => {
    event.preventDefault()
  
    const postId = event.target.dataset.postId
    const likeValue = event.submitter.value
  
    const formData = new FormData(likeForm)
    formData.append('like_value', likeValue)
  
    axios({
      method: "POST",
      url: `/communities/${postId}/likes/`,
      headers: {'X-CSRFToken': csrftoken},
      data: formData
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
        const isDisLiked = response.data.is_disliked
        const likeIcon = likeForm.querySelector('.bi-chevron-up')
        const DisLikeIcon = likeForm.querySelector('.bi-chevron-down')
  
        const likeCount = likeForm.querySelector('.section--likeform--likecount')
  
        likeCount.textContent = response.data.post_like
  
        if (isLiked === true) {
          likeIcon.style.color = 'rgb(0, 185, 222)'
        } else if (isLiked == false) {
          likeIcon.style.color = 'black'
        }
  
        if (isDisLiked === true) {
          DisLikeIcon.style.color = 'rgb(214, 38, 7)'
        } else if (isDisLiked == false) {
          DisLikeIcon.style.color = 'black'
        }
        }
      })
  
      .catch((error) => {
        console.log(error.response)
      })
  })
}

// 디테일 댓글

const commentStartBtn = document.querySelector('.communities--detail--section--commentcreate--btn')
const commentFormDiv = document.querySelector('#communities--detail--section--commentcreate')
const commentCancleBtn = document.querySelector('#communities--detail--section--commentcreate .comment-cancle')

if (commentStartBtn) {
  commentStartBtn.addEventListener('click', (event) => {
    commentStartBtn.style.display = 'none'
    commentFormDiv.style.display = 'block'
  })
}

if (commentCancleBtn) {
  commentCancleBtn.addEventListener('click', (event) => {
    commentStartBtn.style.display = 'flex'
    commentFormDiv.style.display = 'none'
  })
}

// 댓글 수정, 대댓글

document.addEventListener('DOMContentLoaded', function() {
  const CommentlistDiv = document.querySelectorAll('.communities--detail--section--commentitem')
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  CommentlistDiv.forEach((listDiv) => {
    const CommentUpdateForm = listDiv.querySelector('.communities--detail--section--comment--updateform')
    const CommentUpdateSubmitForm = CommentUpdateForm.querySelector('form')
    const CommentCancleBtn = CommentUpdateForm.querySelector('.comment-cancle')
    const RecommentCreateForm = listDiv.querySelector('.communities--detail--section--comment--createform')
    const RecommentCancleBtn = RecommentCreateForm.querySelector('.comment-cancle')

    const CommentUpdateBtn = listDiv.querySelector('.comment--update--button')
    if (CommentUpdateBtn) {
      CommentUpdateBtn.addEventListener('click', (event) => {
        if (CommentUpdateForm.classList.contains('d-none')) {
          CommentUpdateForm.classList.remove('d-none')
        } else {
          CommentUpdateForm.classList.add('d-none')
        }

        if (!RecommentCreateForm.classList.contains('d-none')) {
          RecommentCreateForm.classList.add('d-none')
        }
      })
    }

    if (CommentCancleBtn) {
      CommentCancleBtn.addEventListener('click', (event) => {
        CommentUpdateForm.classList.add('d-none')
      })
    }

    if (CommentUpdateSubmitForm) {
      CommentUpdateSubmitForm.addEventListener('submit', (event) => {
        event.preventDefault()
        const postId = event.target.dataset.postId
        const commentId = event.target.dataset.commentId
        const formData = new FormData(CommentUpdateSubmitForm)
        formData.append('comment-content', CommentUpdateSubmitForm.querySelector('textarea').value)

        axios({
          method: "POST",
          url: `/communities/${postId}/update/${commentId}/`,
          headers: {'X-CSRFToken': csrftoken},
          data: formData,
        })
          .then((response) => {
            const CommentContent = listDiv.querySelector('.communities--detail--comment--content--text')
            CommentContent.textContent = response.data.commentContent

            CommentUpdateForm.classList.add('d-none')
          })
          .catch((error) => {
            console.log(error.response)
          })
      })
    }

    const RecommentCreateBtn = listDiv.querySelector('.recomment--create--button')
    if (RecommentCreateBtn) {
      RecommentCreateBtn.addEventListener('click', (event) => {
        if (RecommentCreateForm.classList.contains('d-none')) {
          RecommentCreateForm.classList.remove('d-none')
        } else {
          RecommentCreateForm.classList.add('d-none')
        }

        if (!CommentUpdateForm.classList.contains('d-none')) {
          CommentUpdateForm.classList.add('d-none')
        }
      })
    }

    if (RecommentCancleBtn) {
      RecommentCancleBtn.addEventListener('click', (event) => {
        RecommentCreateForm.classList.add('d-none')
      })
    }
  })
})
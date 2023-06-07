// 공유

document.addEventListener('DOMContentLoaded', function() {

  document.getElementById('moims--detail--share').addEventListener('click', function() {
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


// 댓글
const commentStartBtn = document.querySelector('.moims--detail--section--commentcreate--btn')
const commentFormDiv = document.querySelector('#moims--detail--section--commentcreate')
const commentCancleBtn = document.querySelector('#moims--detail--section--commentcreate .comment-cancle')

commentStartBtn.addEventListener('click', (event) => {
  commentStartBtn.style.display = 'none'
  commentFormDiv.style.display = 'block'
})

commentCancleBtn.addEventListener('click', (event) => {
  commentStartBtn.style.display = 'flex'
  commentFormDiv.style.display = 'none'
})

// commentFormDiv.addEventListener('submit', async (event) => {
//   event.preventDefault()

// })

// 댓글 수정, 대댓글

document.addEventListener('DOMContentLoaded', function() {
  const CommentlistDiv = document.querySelectorAll('.moims--detail--section--commentitem')
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  CommentlistDiv.forEach((listDiv) => {
    const CommentUpdateForm = listDiv.querySelector('.moims--detail--section--comment--updateform')
    const CommentUpdateSubmitForm = CommentUpdateForm.querySelector('form')
    const CommentCancleBtn = CommentUpdateForm.querySelector('.comment-cancle')
    const RecommentCreateForm = listDiv.querySelector('.moims--detail--section--comment--createform')
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
          url: `/moims/${postId}/update/${commentId}/`,
          headers: {'X-CSRFToken': csrftoken},
          data: formData,
        })
          .then((response) => {
            const CommentContent = listDiv.querySelector('.moims--detail--comment--content--text')
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


// 디테일 좋아요
const likeForm = document.querySelector('#moims--detail--like--form')
const likeAlert = document.querySelector('#moims--detail--alert')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

likeForm.addEventListener('submit', function (event) {
  event.preventDefault()

  const postId = event.target.dataset.postId
  axios({
    method: "POST",
    url: `/moims/${postId}/likes/`,
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

        if (isLiked == true) {
          likeBtnIcon.classList.remove('bi-heart')
          likeBtnIcon.classList.add('bi-heart-fill')

          if (likeAlert.style.display == 'none') {
            const likeAlertH1 = likeAlert.querySelector('h1')
            const likeAlertA = likeAlert.querySelector('a')

            likeAlertH1.textContent = '관심목록에 추가됐어요.'
            likeAlertA.textContent = '관심목록보기'

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
        }

      }
    })

    .catch((error) => {
      console.log(error.response)
    })
})

// 디테일 참여하기
const joinForm = document.querySelector('#moims--detail--join--form')

joinForm.addEventListener('submit', function (event) {
  event.preventDefault()

  const joinFormSubmitText = joinForm.querySelector('button[type="submit"]').textContent
  let isOut = null
  if (joinFormSubmitText == '탈퇴하기') {
    isOut = '1'
  } else {
    isOut = null
  }

  const postId = event.target.dataset.postId
  axios({
    method: "POST",
    url: `/moims/${postId}/joins/?out=${isOut}`,
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
        
        const isJoined = response.data.is_joined
        const joinSubmit = joinForm.querySelector('button[type="submit"]')
        const kakaoBtn1 = joinForm.querySelector('.kakao--btn--1')
        const kakaoBtn2 = joinForm.querySelector('.kakao--btn--2')
        const memberCount1 = document.querySelector('.join--users--count')
        const memberCount2 = document.querySelector('.moims--detail--section--member span')
        const requestUserCarousel = document.querySelector('.request--user--carousel')

        if (isJoined == true) {
          joinSubmit.textContent = '탈퇴하기'
          kakaoBtn2.classList.remove('d-none')
          requestUserCarousel.classList.remove('d-none')
          memberCount1.textContent = parseInt(memberCount1.textContent) + 1
          memberCount2.textContent = parseInt(memberCount2.textContent) + 1

          if (likeAlert.style.display == 'none') {
            const likeAlertH1 = likeAlert.querySelector('h1')
            const likeAlertA = likeAlert.querySelector('a')

            likeAlertH1.textContent = '참여가 완료되었어요!'
            likeAlertA.textContent = '참여모임보기'

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
        } else if (isJoined == false) {
          joinSubmit.textContent = '참여하기'
          requestUserCarousel.classList.add('d-none')
          memberCount1.textContent = parseInt(memberCount1.textContent) - 1
          memberCount2.textContent = parseInt(memberCount2.textContent) - 1

          if (kakaoBtn1) {
            kakaoBtn1.classList.add('d-none')
          }
          kakaoBtn2.classList.add('d-none')
        }

      }
    })

    .catch((error) => {
      console.log(error.response)
    })
})

// 디테일 카카오톡
const kakaoBtns = document.querySelectorAll('.moims--detail--botnavbar--kakao')

kakaoBtns.forEach((btn) => {
  btn.addEventListener('click', (event) => {
    const kakaoUrl = event.target.dataset.kakaoUrl
    window.open(kakaoUrl)
  })
})
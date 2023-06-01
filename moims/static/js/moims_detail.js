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


// 댓글 비동기
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
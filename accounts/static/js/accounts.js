// 주소검색

function search_address() {
  new daum.Postcode({
    oncomplete: function(data) {
      const addr = data.address;
      document.getElementById("s_address").value = addr;
      const addt = data.bname;
      document.getElementById("t_address").value = addt;
      const addb = data.buildingName;
      document.getElementById("b_address").value = addb;
      updateMap(addr);
    }
  
  }).open();
  
}

// 변경시 알람
function finish(event) {
  event.preventDefault(); 
  alert("성공적으로 변경되었습니다.");
  var form = event.target;
  form.submit();
}

// url 복사
function copy_trackback(url) {
  var tempInput = document.createElement('input');
  tempInput.value = url;
  document.body.appendChild(tempInput);
  tempInput.select();
  document.execCommand('copy');
  document.body.removeChild(tempInput);
  alert('URL이 복사되었습니다.');
}

// 자기소개 폼
document.addEventListener("DOMContentLoaded", function() {
  var toggleButton = document.getElementById("introduce-toggle");
  var cancelButton = document.getElementById("introduce-cancel");
  var introduceBox = document.querySelector(".introduce--box");

  if (toggleButton) {
    toggleButton.addEventListener("click", function() {
      introduceBox.classList.toggle("show--form");
    });
  }

  if (cancelButton) {
    cancelButton.addEventListener("click", function() {
      introduceBox.classList.remove("show--form");
    });
  }
});


// 유저 평가
const likesForm = document.querySelector('#user-likes-form');
const dislikesForm = document.querySelector('#user-dislikes-form');
const u_l_csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const u_d_csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
if (likesForm) {
  var uUsername = likesForm.dataset.username;
}

if (likesForm) {
  likesForm.addEventListener('submit', function (event) {
    event.preventDefault();
  
    axios({
      method: 'post',
      url: `/accounts/profile/${uUsername}/likes/`,
      headers: { 'X-CSRFToken': u_l_csrftoken },
    })
      .then((response) => {
        const uisLiked = response.data.u_is_liked;
        const userlikesCountSpan = document.querySelector('#user-likes-count');
        const thumbsupIcon = document.querySelector('#user-up');
        const dislikeForm = document.querySelector('#user-dislikes-form');
        const maumParagraph = document.querySelector('.maum p');
  
        if (uisLiked) {
          thumbsupIcon.classList.remove('bi-emoji-smile');
          thumbsupIcon.classList.add('bi-emoji-smile-fill');
          dislikeForm.querySelector('button').disabled = true;
          dislikeForm.querySelector('button').style.color = 'gray';
        } else {
          thumbsupIcon.classList.remove('bi-emoji-smile-fill');
          thumbsupIcon.classList.add('bi-emoji-smile');
          dislikeForm.querySelector('button').disabled = false;
          dislikeForm.querySelector('button').style.color = '';
        }
  
        userlikesCountSpan.textContent = response.data.user_likes_count;
        maumParagraph.textContent = `${response.data.maum.toFixed(1)}cm`;
      })
      .catch((error) => {
        console.error(error);
      });
  });
}

if (dislikesForm) {
  dislikesForm.addEventListener('submit', function (event) {
    event.preventDefault();
  
    axios({
      method: 'post',
      url: `/accounts/profile/${uUsername}/dislikes/`,
      headers: { 'X-CSRFToken': u_d_csrftoken },
    })
      .then((response) => {
        const uisdisLiked = response.data.u_is_disliked;
        const userdislikesCountSpan = document.querySelector('#user-dislikes-count');
        const thumbsdownIcon = document.querySelector('#user-down');
        const likeForm = document.querySelector('#user-likes-form');
        const maumParagraph = document.querySelector('.maum p');
  
        if (uisdisLiked) {
          thumbsdownIcon.classList.remove('bi-emoji-neutral');
          thumbsdownIcon.classList.add('bi-emoji-neutral-fill');
          likeForm.querySelector('button').disabled = true;
          likeForm.querySelector('button').style.color = 'gray';
        } else {
          thumbsdownIcon.classList.remove('bi-emoji-neutral-fill');
          thumbsdownIcon.classList.add('bi-emoji-neutral');
          likeForm.querySelector('button').disabled = false;
          likeForm.querySelector('button').style.color = '';
        }
  
        userdislikesCountSpan.textContent = response.data.user_dislikes_count;
        maumParagraph.textContent = `${response.data.maum.toFixed(1)}cm`; 
      })
      .catch((error) => {
        console.error(error);
      });
  });
}

function previewImage(event) {
  var input = event.target;
  if (input.files && input.files.length > 0) {
    var previewContainer = document.querySelector('#preview-container');
    previewContainer.innerHTML = '';

    for (var i = 0; i < input.files.length; i++) {
      var reader = new FileReader();
      reader.onload = function(e) {
        var preview = document.createElement('img');
        preview.setAttribute('src', e.target.result);
        preview.setAttribute('class', 'preview-image');
        previewContainer.appendChild(preview);
      };
      reader.readAsDataURL(input.files[i]);
    }

    previewContainer.style.display = 'flex';
  }
}

var imageInput = document.querySelector('#id_image_first');
if (imageInput) {
  imageInput.addEventListener('change', previewImage);
}
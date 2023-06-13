const form = document.querySelector('#follow-form');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
if (form) {
  var personId = form.dataset.userId;
  var personUsername = form.dataset.username;
}
const followingsCountTag = document.querySelector('#followings-count');
const followersCountTag = document.querySelector('#followers-count');
const followerList = document.querySelector('#follower-ul');

if (form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const userId = event.target.dataset.userId;
  
    axios({
      method: 'post',
      url: `/accounts/${userId}/follow/`,
      headers: { 'X-CSRFToken': csrftoken },
    })
      .then((response) => {
        const isFollowed = response.data.is_followed;
        const followBtn = document.querySelector('#follow-form > input[type=submit]');
        if (isFollowed === true) {
          followBtn.value = '언팔로우';
        } else {
          followBtn.value = '팔로우';
        }
        const followingsCountData = response.data.followings_count;
        const followersCountData = response.data.followers_count;
        followingsCountTag.textContent = followingsCountData;
        followersCountTag.textContent = followersCountData;
  
  
        // 업데이트된 팔로워 목록을 가져와서 템플릿에 반영
        updateFollowerList(personUsername);
      })
      .catch((error) => {
        console.error(error);
      });
  });
}

// 팔로워 리스트 업데이트 함수
function updateFollowerList(username) {
  axios.get(`/accounts/profile/${username}/followers-list/`)
    .then((response) => {
      followerList.innerHTML = response.data;
    })
    .catch((error) => {
      console.error(error);
    });
}

// 페이지 로드 시 팔로잉/팔로워 목록 초기화
if (personUsername) {
  window.addEventListener('DOMContentLoaded', () => {
    const username = personUsername;
    updateFollowerList(username);
  });
}  

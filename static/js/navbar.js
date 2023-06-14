window.addEventListener("scroll", function() {
  let navbar = document.querySelector(".nav--bar");
  let svgPaths = document.querySelectorAll(".nav--logo svg path");

  navbar.classList.toggle('scrolled', window.scrollY > 10);

  if (window.scrollY > 10) {
    svgPaths.forEach(path => path.setAttribute("stroke", "#ffffff"));
  } else {
    svgPaths.forEach(path => path.setAttribute("stroke", "#34568b"));
  }
});
/* 사용자가 스크롤을 10px만큼 내리면 nav 속성이 변합니다 */


/* 화면을 늘리고 모바일 메뉴가 활성화 된 뒤에 다시 화면을 클렸을때 모바일 메뉴를 감춤 */ 
// window.addEventListener("resize", function() {
//     if(window.innerWidth > 768) {
//         mobileMenu.style.display = "none";
//     }
// });


document.addEventListener('DOMContentLoaded', function() {
    const modal = document.querySelector('#bot_nav--modal');
    const modalContent = modal.querySelector('.bot_nav--modal--content');
    const profileIcon = document.querySelector('#bot_nav--profile--icon');
    const navBar = document.querySelector('.bottom--nav');
  
    if (profileIcon) {
      profileIcon.addEventListener('click', function(event) {
        event.stopPropagation(); //이벤트 전파 방지 (이게 없으면 하단네비바 클릭시 모달 안사라짐)
        modal.classList.toggle('show');
        modalContent.classList.toggle('show');
      });
    }
  
  
    // 모달창 어디든 클릭하면 비활성화 시킴
    if (modal) {
      modal.addEventListener('click', function(e) {
        if (e.target === this) {
          this.classList.remove('show');
          modalContent.classList.remove('show');
        }
      });
    }
  
    // 모달 활성화시 하단메뉴 영역을 클릭해도 비활성화 시킴
    if (navBar) {
      navBar.addEventListener('click', function() {
        if (modal.classList.contains('show')) {
          modal.classList.remove('show');
          modalContent.classList.remove('show');
        }
      });
    }
  
    // 브라우저 크기 변경 이벤트
    window.addEventListener('resize', function() {
      if (modal.classList.contains('show')) {
        modal.classList.remove('show');
        modalContent.classList.remove('show');
      }
    });
  });

// 네비바 오른쪽 콜랩스

const navbarImageBtn = document.querySelector('.nav--bar--right--image')
const navbarCollapse = document.querySelector('#nav--bar--right--collapse')

const navbarBellBtn = document.querySelector('.nav--bar--bell--a')
const navbarBellCollapse = document.querySelector('#nav--bar--bell--collapse')

if (navbarImageBtn) {
  navbarImageBtn.addEventListener('mouseenter', (event) => {
    navbarCollapse.classList.remove('d-none')
  })
}

if (navbarImageBtn) {
  navbarImageBtn.addEventListener('mouseleave', function(event) {
    if (!event.relatedTarget || !navbarCollapse.contains(event.relatedTarget)) {
      if (!navbarCollapse.classList.contains('d-none')) {
        navbarCollapse.classList.add('d-none')
      }
    }
  })
}

if (navbarCollapse) {
  navbarCollapse.addEventListener('mouseleave', function(event) {
    if (!event.relatedTarget || !navbarImageBtn.contains(event.relatedTarget)) {
      if (!navbarCollapse.classList.contains('d-none')) {
        navbarCollapse.classList.add('d-none')
      }
    }
  })
}

if (navbarBellBtn) {
  navbarBellBtn.addEventListener('mouseenter', (event) => {
    navbarBellCollapse.classList.remove('d-none')
  })
}

if (navbarBellBtn) {
  navbarBellBtn.addEventListener('mouseleave', function(event) {
    if (!event.relatedTarget || !navbarBellCollapse.contains(event.relatedTarget)) {
      if (!navbarBellCollapse.classList.contains('d-none')) {
        navbarBellCollapse.classList.add('d-none')
      }
    }
  })
}

if (navbarBellCollapse) {
  navbarBellCollapse.addEventListener('mouseleave', function(event) {
    if (!event.relatedTarget || !navbarImageBtn.contains(event.relatedTarget)) {
      if (!navbarBellCollapse.classList.contains('d-none')) {
        navbarBellCollapse.classList.add('d-none')
      }
    }
  })
}

var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
var loginSocket;
var navAlarmSocket;
var indexSocket;

if (!loginSocket || loginSocket.readyState !== WebSocket.OPEN) { 
  // 만약 소켓이 없으면 소켓 생성 -> 로그인을 의미하는 socket생성
  loginSocket = new WebSocket(protocol + '//' + window.location.host + '/ws/login/');
}
if (!navAlarmSocket || navAlarmSocket.readyState !== WebSocket.OPEN) { 
  // 만약 소켓이 없으면 소켓 생성 -> 로그인을 의미하는 socket생성
  navAlarmSocket = new WebSocket(protocol + '//' + window.location.host + '/ws/alarm/');
}
if (!indexSocket || indexAlarmSocket.readyState !== WebSocket.OPEN) { 
  // 만약 소켓이 없으면 소켓 생성 -> 로그인을 의미하는 socket생성
  indexSocket = new WebSocket(protocol + '//' + window.location.host + '/ws/index/');
}
const currentUser2 = document.getElementById('currentUser').value;

loginSocket.onopen = () => {
  console.log('loginSocket connection established.');
};

navAlarmSocket.onopen = () => {
  console.log('alarmSocket connection established.');
};

navAlarmSocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data)
  const sender = data.sender
  const retriever = data.retriever
  const content = data.content
  const sendername = data.sendername
  
  const segments = chatSocket.url.split('/');
  const chatroomId = segments[segments.length - 2];

  fetch(`/chats/get_chatroom_data/${chatroomId}/`)
  .then(function(response) {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Failed to fetch chatroom data');
    }
  })
  .then(function(data) {
    // 데이터 사용
    var user1 = data.user1;
    var user2 = data.user2;
    console.log(user1, user2);
  })
  .catch(function(error) {
    console.error(error);
  });
  
  if (typeof chatSocket !== 'undefined' && (user1 === sender || user2 === sender)) { // + url의 맨 뒤가 sender와 같으면
    
  } else {
    if (retriever == currentUser2) {
      // 만약 위에가 sendername이 같다면 위에서 숫자만 추가한다.
  
      const navBarBellCollapse = document.querySelector('#nav--bar--bell--collapse');
      const aTags = navBarBellCollapse.querySelectorAll('a');
  
      if (aTags.length >= 5) {
        aTags[4].remove(); // 첫 번째 <a> 태그 제거
      }
  
      const newAlarm = document.createElement('a');
      newAlarm.href = `/chats/${sendername}`;
      newAlarm.innerHTML = `<span>${sendername}</span>님이 메세지를 보냈어요.`;
      
      const firstLink = navBarBellCollapse.querySelector('a');
      if (firstLink) {
        // 첫 번째 링크가 있을 경우 앞에 추가
        navBarBellCollapse.insertBefore(newAlarm, firstLink);
      } else {
        // 링크가 없을 경우 맨 뒤에 추가
        navBarBellCollapse.appendChild(newAlarm);
      }
  
      document.querySelector('.nav--bar--bell--red').classList.remove('d-none');
    }
  }
  
  loginSocket.onclose = () => {
    console.log('loginSocket connection closed.');
  };
  navAlarmSocket.onclose = () => {
    console.log('alarmSocket connection closed.');
  };
};
window.addEventListener("scroll", function() {
    let navbar = document.querySelector(".nav--bar");
    navbar.classList.toggle('scrolled', window.scrollY > 10);
});
/* 사용자가 스크롤을 10px만큼 내리면 nav 속성이 변합니다 */

let hamburger = document.querySelector(".hamburger--menu");
let mobileMenu = document.querySelector(".mobile-menu");

mobileMenu.style.display = "none"; 

hamburger.addEventListener("click", function() {
    mobileMenu.style.display = mobileMenu.style.display === "none" ? "flex" : "none";
});

/* 화면을 늘리고 모바일 메뉴가 활성화 된 뒤에 다시 화면을 클렸을때 모바일 메뉴를 감춤 */ 
window.addEventListener("resize", function() {
    if(window.innerWidth > 768) {
        mobileMenu.style.display = "none";
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const modal = document.querySelector('#bot_nav--modal');
    const modalContent = modal.querySelector('.bot_nav--modal--content');
    const profileIcon = document.querySelector('#bot_nav--profile--icon');
    const navBar = document.querySelector('.bottom--nav');
  
    profileIcon.addEventListener('click', function(event) {
      event.stopPropagation(); //이벤트 전파 방지 (이게 없으면 하단네비바 클릭시 모달 안사라짐)
      modal.classList.toggle('show');
      modalContent.classList.toggle('show');
    });
  
  
    // 모달창 어디든 클릭하면 비활성화 시킴
    modal.addEventListener('click', function(e) {
      if (e.target === this) {
        this.classList.remove('show');
        modalContent.classList.remove('show');
      }
    });
  
    // 모달 활성화시 하단메뉴 영역을 클릭해도 비활성화 시킴
    navBar.addEventListener('click', function() {
      if (modal.classList.contains('show')) {
        modal.classList.remove('show');
        modalContent.classList.remove('show');
      }
    });
  
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

navbarImageBtn.addEventListener('mouseenter', (event) => {
  navbarCollapse.classList.remove('d-none')
})

navbarImageBtn.addEventListener('mouseleave', function(event) {
  if (!event.relatedTarget || !navbarCollapse.contains(event.relatedTarget)) {
    if (!navbarCollapse.classList.contains('d-none')) {
      navbarCollapse.classList.add('d-none')
    }
  }
})

navbarCollapse.addEventListener('mouseleave', function(event) {
  if (!event.relatedTarget || !navbarImageBtn.contains(event.relatedTarget)) {
    if (!navbarCollapse.classList.contains('d-none')) {
      navbarCollapse.classList.add('d-none')
    }
  }
})
window.addEventListener("scroll", function() {
    let navbar = document.querySelector(".navbar");
    console.log(navbar); 
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

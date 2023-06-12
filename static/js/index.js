// $(document).ready(function() {
//     $(window).scroll(function(){
//         let scroll = $(window).scrollTop(),
//             slowScroll = scroll/2, //현재 스크롤을 절반으로 줄임
//             slowBg = '100% ' + -(slowScroll) + 'px'; // 스크롤이 움직일때마다 배경화면도 같이 절반 속도로 움직임 

//         console.log("Scroll event triggered, scroll position: " + scroll);

//         $('.text#text1').css({transform: "translateY(" + (-scroll/3) + "px)"});
//         $('.text#text2').css({transform: "translateY(" + (-scroll/5) + "px)"});
//         $('.parallax').css({backgroundPosition: slowBg});
//     });
// });

// 인덱스 배너
var parallax = document.querySelector('.parallax');
var bannerImg = parallax.querySelector('.index--banner_img');

// Attach an event listener to the scroll event
window.addEventListener('scroll', function() {
    // Calculate the scroll position
    var scrollPosition = window.pageYOffset;

    // Apply the scroll effect by adjusting the top position of the image
    if (bannerImg) {
        bannerImg.style.transform = 'translateY(' + scrollPosition * 0.5 + 'px)';
    }
});


// ScrollOut({ });
let observer = new IntersectionObserver((e)=>{
    e.forEach((box)=>{
        if(box.isIntersecting) {
           box.target.style.opacity = "1"; 
           box.target.style.transform = "translateY(0) scale(1)"; 
        } else {
            box.target.style.opacity = "0"; 
        }            
    })
})
let div = document.querySelectorAll('.index--section')
observer.observe(div[0])
observer.observe(div[1])
observer.observe(div[2])
// observer.observe(div[3])
let maumNum = document.querySelectorAll('.index--maum_num')
observer.observe(maumNum[0])
observer.observe(maumNum[1])
observer.observe(maumNum[2])
observer.observe(maumNum[3])
observer.observe(maumNum[4])
observer.observe(maumNum[5])

$(document).ready(function(){
    $(".owl-carousel").owlCarousel({
    	loop:true,
      margin:10,
      nav:true,
      center: true,
      navText: [
  	    "<i class='fa fa-angle-left'></i>",
  	    "<i class='fa fa-angle-right'></i>"
  	],
      responsive:{
          0:{
              items:1
          },
          600:{
              items:1
          },
          1000:{
              items:3
          }
      }
    });
  });
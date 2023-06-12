document.addEventListener("DOMContentLoaded", function() {
  var moim1Button = document.getElementById("moim1");
  var moim2Button = document.getElementById("moim2");
  var moim3Button = document.getElementById("moim3");
  var moim1 = document.querySelector(".moim1");
  var moim2 = document.querySelector(".moim2");
  var moim3 = document.querySelector(".moim3");
  
  moim1.style.display = "block";
  moim2.style.display = "none";
  moim3.style.display = "none";

  moim1Button.addEventListener("click", function() {
    moim1.style.display = "block";
    moim2.style.display = "none";
    moim3.style.display = "none";
    if (request_user === person) {
    moim1Button.classList.add("ylw");
    moim2Button.classList.remove("ylw");
    moim3Button.classList.remove("ylw");
  }
  });

  moim2Button.addEventListener("click", function() {
    moim1.style.display = "none";
    moim2.style.display = "block";
    moim3.style.display = "none";
    moim1Button.classList.remove("ylw");
    moim2Button.classList.add("ylw");
    moim3Button.classList.remove("ylw");
  });

  moim3Button.addEventListener("click", function() {
    moim1.style.display = "none";
    moim2.style.display = "none";
    moim3.style.display = "block";
    moim1Button.classList.remove("ylw");
    moim2Button.classList.remove("ylw");
    moim3Button.classList.add("ylw");
  });
});

document.addEventListener("DOMContentLoaded", function() {
  var shop1Button = document.getElementById("shop1");
  var shop2Button = document.getElementById("shop2");
  var shop1 = document.querySelector(".shop1");
  var shop2 = document.querySelector(".shop2");
  
  shop1.style.display = "block";
  shop2.style.display = "none";

  shop1Button.addEventListener("click", function() {
    shop1.style.display = "block";
    shop2.style.display = "none";
    if (request_user === person) {
    shop1Button.classList.add("ylw");
    shop2Button.classList.remove("ylw");
    }
  });

  shop2Button.addEventListener("click", function() {
    shop1.style.display = "none";
    shop2.style.display = "block";
    shop1Button.classList.remove("ylw");
    shop2Button.classList.add("ylw");
  });
});

document.addEventListener("DOMContentLoaded", function() {
  var cmty1Button = document.getElementById("cmty1");
  var cmty2Button = document.getElementById("cmty2");
  var cmty1 = document.querySelector(".cmty1");
  var cmty2 = document.querySelector(".cmty2");
  
  cmty1.style.display = "block";
  cmty2.style.display = "none";

  cmty1Button.addEventListener("click", function() {
    cmty1.style.display = "block";
    cmty2.style.display = "none";
    if (request_user === person) {
    cmty1Button.classList.add("ylw");
    cmty2Button.classList.remove("ylw");
    }
  });

  cmty2Button.addEventListener("click", function() {
    cmty1.style.display = "none";
    cmty2.style.display = "block";
    cmty1Button.classList.remove("ylw");
    cmty2Button.classList.add("ylw");
  });
});

function initializeShowMore(btnClass, itemClass) {
  const items = document.querySelectorAll(`.${itemClass}`);
  const btnMore = document.querySelector(`.${btnClass}`);
  const hideClass = 'hide';
  const showMoreText = '더보기';
  const showLessText = '간략히';

  let visibleItems = 4;

  function showNextItems() {
    for (let i = visibleItems; i < visibleItems + 4 && i < items.length; i++) {
    items[i].classList.remove(hideClass);
  }
  visibleItems += 4;
  if (visibleItems >= items.length) {
    btnMore.textContent = showLessText;
  }
}
  function hideExtraItems() {
    for (let i = visibleItems; i < items.length; i++) {
      items[i].classList.add(hideClass);
    }
    btnMore.textContent = showMoreText;
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  }

  hideExtraItems();

  btnMore.addEventListener('click', function() {
    if (visibleItems < items.length) {
      showNextItems();
    } else {
      visibleItems = 4;
      hideExtraItems();
    }
  });

  if (items.length <= visibleItems) {
    btnMore.classList.add(hideClass);
  } else {
    btnMore.classList.remove(hideClass);
  }
}

const writeMoimItems = document.querySelectorAll('.write-moim');
const likeMoimItems = document.querySelectorAll('.like-moim');
const joinMoimItems = document.querySelectorAll('.join-moim');
const writeMarketItems = document.querySelectorAll('.write-market');
const likeMarketItems = document.querySelectorAll('.like-market');
const writeCommunityItems = document.querySelectorAll('.write-community');
const scrapeCommunityItems = document.querySelectorAll('.scrape-community');

if (writeMoimItems.length > 4) {
  initializeShowMore('btn-more1', 'write-moim');
}
if (likeMoimItems.length > 4) {
  initializeShowMore('btn-more2', 'like-moim');
}
if (joinMoimItems.length > 4) {
  initializeShowMore('btn-more3', 'join-moim');
}
if (writeMarketItems.length > 4) {
  initializeShowMore('btn-more4', 'write-market');
}
if (likeMarketItems.length > 4) {
  initializeShowMore('btn-more5', 'like-market');
}
if (writeCommunityItems.length > 4) {
  initializeShowMore('btn-more6', 'write-community');
}
if (scrapeCommunityItems.length > 4) {
  initializeShowMore('btn-more7', 'scrape-community');
}
//메세지가 오면 onmessage가 로그인은 없으니 로그인을 이용해서 하자 로그인이 온 sender가 상대방인데 그때 id를 골라서맨 위로 올리기

indexSocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const sender = data.sender
  const retriever = data.retriever
  const message = data.message
  const sendername = data.sendername
  const senderImage = data.senderImage  
  const parentElement = document.querySelector('.chats--container')
  const senderElement = document.querySelector(`#${sender}`)

  
  if (currentUser5 == retriever) {
    if (senderElement) {
      senderElement.querySelector('.chat--message').textContent = `${message}`
      senderElement.querySelector('.chat--created').textContent = '방금 전'

      const notificationElement = senderElement.querySelector('.chat--notification')

      notificationElement.style.display = 'block';
      
      notificationElement.textContent = parseInt(notificationElement.textContent) + 1

      parentElement.insertBefore(senderElement, parentElement.children[1]);
      
    } else {
      const newChat = document.createElement('a');
      newChat.href = `/chats/${sendername}/`;
      newChat.className = 'chat--link';
      newChat.id = `${sender}`;

      newChat.innerHTML = `
          <div class="chat--box">
            <div class="chat--profile">
              <img src="${senderImage}" alt="profile_image">
            </div>
            <p class="status--login status--log" id="user${sender}"></p>
            <p class="status--log" id="user${sender}Sub"></p>
            <div class='chat--notification'>1</div>
            <div class="chat--txt">
              <div>
                ${sendername}
              </div>
              <div class="chat--txt--info">
                <span class="chat--message">${message}</span>
                <span class="chat--created">방금 전</span>
              </div>
            </div>
          </div>
      `;    
      
      if(parentElement.children[1]) {
        parentElement.insertBefore(newChat, parentElement.children[1]);
      }
      else {
        parentElement.appendChild(newChat);
      }
    }
  }
}

let loginStatusTimeout = null; // Variable to store the timeout ID
let isLoginStatusPresent = true; // Flag variable to track the presence of login status
let isLoggedOut = false; // Flag variable to track the logged-out state

loginSocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const loginUser = data.loginUser;
  const loginStatus = data.loginStatus;

  clearTimeout(loginStatusTimeout); // Clear the previous timeout

  const element = document.querySelector(`#user${loginUser}`);
  const subElement = document.querySelector(`#user${loginUser}Sub`);

  if (loginStatus && element && subElement) {
    element.classList.remove('status--logout');
    element.classList.add('status--login');

    subElement.classList.remove('status--log--black');
    subElement.classList.add('status--log');

    isLoginStatusPresent = true;
    isLoggedOut = false;
  } else if (element && subElement) {
    isLoggedOut = true;

    // Set a new timeout for 3 seconds if the user is logged out
      loginStatusTimeout = setTimeout(() => {
        isLoginStatusPresent = false; // Set the flag to false before invoking the function

        if (isLoggedOut && !isLoginStatusPresent) {
          updateLoginStatus(loginUser);
        }
      }, 3000);
  }
};

// Function to update the login status to "logout"
function updateLoginStatus(loginUser) {
  // Perform the desired action to show the logged-out status
  const element = document.querySelector(`#user${loginUser}`);
  const subElement = document.querySelector(`#user${loginUser}Sub`);

  if (element && subElement) {
    element.classList.remove('status--login');
    element.classList.add('status--logout');

    subElement.classList.remove('status--log');
    subElement.classList.add('status--log--black');
  }
}

// Set the initial timeout for 3 seconds
loginStatusTimeout = setTimeout(() => {
  if (isLoggedOut && !isLoginStatusPresent) {
    updateLoginStatus(loginUser);
  }
  isLoginStatusPresent = false; // Reset the flag after 3 seconds
}, 3000);
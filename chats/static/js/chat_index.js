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

loginSocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const loginUser = data.loginUser
  const loginStatus = data.loginStatus
  
  const element = document.querySelector(`#user${loginUser}`);
  const subElement = document.querySelector(`#user${loginUser}Sub`);
  if (loginStatus) {
    element.classList.remove('status--logout');
    element.classList.add('status--login');

    subElement.classList.remove('status--log--black');
    subElement.classList.add('status--log');
  } else {
    element.classList.remove('status--login');
    element.classList.add('status--logout');

    subElement.classList.remove('status--log');
    subElement.classList.add('status--log--black');
    // status--log--black 추가
  }
};

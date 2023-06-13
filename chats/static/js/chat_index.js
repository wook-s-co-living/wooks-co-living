//메세지가 오면 onmessage가 로그인은 없으니 로그인을 이용해서 하자 로그인이 온 sender가 상대방인데 그때 id를 골라서맨 위로 올리기


indexSocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const sender = data.sender
  const retriever = data.retriever
  const message = data.message
  const sendername = data.sendername
  const senderImage = data.senderImage
  const parentElement = document.querySelector('.chats--container')
  
  // 만약 위에가 sendername이 같다면 위에서 숫자만 추가한다.
  const senderElement = document.querySelector(`#${sender}`)
  
  if (senderElement) {
    senderElement.querySelector('.chat--message').textContent = `${message}`
    senderElement.querySelector('.chat--created').textContent = '방금 전'
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

    parentElement.insertBefore(newChat, parentElement.children[1]);
  }

}

loginSocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const loginUser = data.loginUser
  const loginStatus = data.loginStatus
  const element = document.querySelector(`#user${loginUser}`);
  console.log("도달1")
  if (loginUser == "{{user}}") {
  console.log("도달2")
} else if (loginStatus) {
    console.log("도달3")
    element.classList.remove('status--logout');
    element.classList.add('status--login');
    element.textContent = '활성화';
  } else {
    element.classList.remove('status--login');
    element.classList.add('status--logout');
    element.textContent = '비활성화';
  }
  console.log(`#user${loginUser}`)
};




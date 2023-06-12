const roomName = JSON.parse(document.getElementById('room-name').textContent);
      
const chatSocket = new WebSocket(
'ws://'
+ window.location.host
+ '/ws/chat/'
+ roomName
+ '/'
);

const currentUser = document.getElementById('currentUser').value;
const retriever = document.getElementById('retriever').value;
const retrieverName = document.getElementById('retriever_name').value;

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const sender = data.sender;  // 발신자 정보를 받아옵니다.

    // 현재 사용자와 발신자가 동일한지 확인합니다.
    const isCurrentUser = (sender === currentUser);
    
    if (isCurrentUser) {
        // 발신자가 현재 사용자인 경우 오른쪽에 채팅을 배치합니다.
        document.querySelector('#chat-log').innerHTML += '<div class="chat-bubble chat-right"><span data-sender="' + sender + '"></span><div class="d-flex align-items-end"><span class="right--time">' + getCurrentTime() + '</span><p>' + message + '</p></div></div>';
    } else {
        const chatLog = document.querySelector('#chat-log');

        // 이전 메시지의 발신자 가져오기
        const lastMessage = chatLog.lastElementChild;
        const previousSender = lastMessage ? lastMessage.querySelector('span').dataset.sender : null;

        const messageBox = document.createElement('div');
        messageBox.className = 'message--box';

				const senderInfo = document.createElement('span');
				senderInfo.dataset.sender = sender;
				messageBox.appendChild(senderInfo);

        const profileSub = document.createElement('div');
        profileSub.className = 'chat--profile--sub';

        // 이전 발신자와 현재 발신자가 다른 경우 이미지 삽입
        if (previousSender !== sender) {
            const image = document.createElement('img');
            image.alt = 'profile_image';
						image.src = imageUrl;
            profileSub.appendChild(image);
        }

        const chatBubble = document.createElement('div');
        chatBubble.className = 'chat-bubble chat-left';
        const messageParagraph = document.createElement('p');
        messageParagraph.textContent = message;
        chatBubble.appendChild(messageParagraph);

				const timeSpan = document.createElement('span');
				timeSpan.className = 'left--time';
				timeSpan.textContent = getCurrentTime();
				chatBubble.appendChild(timeSpan);

        messageBox.appendChild(profileSub);
        messageBox.appendChild(chatBubble);

        chatLog.appendChild(messageBox);
    }
		scrollToBottom();
};


chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) { 
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'roomName': roomName,
        'message': message,
        'sender': currentUser,
        'retriever': retriever,
    }));
    
    navAlarmSocket.send(JSON.stringify({
        'message': message,
        'sender': currentUser,
        'retriever': retriever,
        'roomName': roomName,
    }))

    indexSocket.send(JSON.stringify({
        'message': message,
        'sender': currentUser,
        'retriever': retriever,
        'roomName': roomName,
    }))

    loginSocket.send(JSON.stringify({
        'message': message,
        'sender': currentUser,
        'retriever': retriever,
        'roomName': roomName,
    }))
    
messageInputDom.value = '';
};

function getCurrentTime() {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  return hours + ':' + minutes;
}

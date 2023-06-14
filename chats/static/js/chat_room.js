const roomName = JSON.parse(document.getElementById('room-name').textContent);
protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'; 
const chatSocket = new WebSocket(
protocol
+ '//'
+ window.location.host
+ '/ws/chat/'
+ roomName
+ '/'
);

const currentUser = document.getElementById('currentUser').value;
const retriever = document.getElementById('retriever').value;
const retrieverName = document.getElementById('retriever_name').value;

function updateLatestMessage(retrieverId, senderId) {

}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
    }

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const message = data.message;
        const sender = data.sender;
        const retriever = data.retriever;
        const senderId = data.senderId;
        const retrieverId = data.retrieverId;
        
        
        // 현재 사용자와 발신자가 동일한지 확인합니다.
        const isCurrentUser = (sender === currentUser);
        
        if (isCurrentUser) { // 내가 발신자면
            document.querySelector('#chat-log').innerHTML += '<div class="chat-bubble chat-right"><span data-sender="' + sender + '"></span><div class="d-flex align-items-end"><span class="right--time">' + getCurrentTime() + '</span><p>' + message + '</p></div></div>';
        } else { // 내가 수신자면
            
        var dataset = {
            retriever: retriever,
            sender: sender,
        
            hi: "hihi"
        };
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/chats/update_latest_message/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        
        var csrftoken = getCookie('csrftoken');
        
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.onload = function () {
            if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
        }
        };
        xhr.send(JSON.stringify(dataset));
        

        const chatLog = document.querySelector('#chat-log');
        const lastMessage = chatLog.lastElementChild;
        const previousSender = lastMessage ? lastMessage.querySelector('span').dataset.sender : null;

        const messageBox = document.createElement('div');
        messageBox.className = 'message--box';

				const senderInfo = document.createElement('span');
				senderInfo.dataset.sender = sender;
				messageBox.appendChild(senderInfo);

        const profileSub = document.createElement('div');
        profileSub.className = 'chat--profile--sub';

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

    liveAlarmSocket.send(JSON.stringify({
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

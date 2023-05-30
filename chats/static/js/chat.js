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
        const isCurrentUser = (sender === currentUser);  // currentUser는 현재 사용자의 정보입니다.
        
        if (isCurrentUser) {
            // 발신자가 현재 사용자인 경우 오른쪽에 채팅을 배치합니다.
            document.querySelector('#chat-log').innerHTML += '<div class="chat-bubble chat-right"> 나 : ' + message + '</div>';
        } else {
            // 발신자가 현재 사용자가 아닌 경우 왼쪽에 채팅을 배치합니다.
            document.querySelector('#chat-log').innerHTML += '<div class="chat-bubble chat-left"> ' + retrieverName + ' : ' + message + '</div>';
        }
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

        messageInputDom.value = '';
    };
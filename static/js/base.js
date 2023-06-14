liveAlarmSocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data)
  const sender = data.sender
  const retriever = data.retriever
  const message = data.message
  const sendername = data.sendername
  var currentURL = window.location.href;
  console.log(currentURL);
  const decodedString = decodeURIComponent(currentURL);
  const segments = decodedString.split('/');
  const chatroomId = segments[segments.length - 2];
  console.log(decodedString);
  console.log(chatroomId);
  console.log(sendername)
  
  if(chatroomId == sendername){

  }else{
    if (retriever == currentUser2) {
      // 만약 위에가 sendername이 같다면 위에서 숫자만 추가한다.
  
      const bodyElement  = document.querySelector('body');
      const sideElement = document.querySelector('#side-alarm')
      const newAlarm = document.createElement('a');

      if (window.innerWidth < 800) {
        newAlarm.href = `/chats/${sendername}`;
        newAlarm.classList.add('livealarm')
        newAlarm.innerHTML = `<span><i class="bi bi-chat-fill"></i> ${sendername}</span>님이 메세지를 보냈어요.`;
        
        bodyElement.insertBefore(newAlarm, bodyElement.lastChild);

        setTimeout(() => {
          bodyElement.removeChild(newAlarm);
        }, 3000);
      } else {
        newAlarm.href = `/chats/${sendername}`;
        newAlarm.classList.add('sidelivealarm')
        newAlarm.innerHTML = `<div><s><i class="bi bi-chat-fill"></i> ${sendername}</s>님이 메세지를 보냈어요.</div><section>${message}</section>`;
        
        sideElement.insertBefore(newAlarm, sideElement.firstChild);

        setTimeout(() => {
          sideElement.removeChild(newAlarm);
        }, 3000);
      }

      
    }

  };
  loginSocket.onclose = () => {
    console.log('loginSocket connection closed.');
  };
  navAlarmSocket.onclose = () => {
    console.log('alarmSocket connection closed.');
  };
};
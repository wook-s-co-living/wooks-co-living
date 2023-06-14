liveAlarmSocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data)
  const sender = data.sender
  const retriever = data.retriever
  const content = data.content
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
  
      const parentElement  = document.querySelector('#livealarm');
  
      const newAlarm = document.createElement('a');
      newAlarm.href = `/chats/${sendername}`;
      newAlarm.innerHTML = `<span>${sendername}</span>님이 메세지를 보냈어요.`;
      
      parentElement.insertBefore(newAlarm, parentElement.firstChild);
      
      setTimeout(() => {
        parentElement.removeChild(newAlarm);
      }, 3000);
    }

  };
  loginSocket.onclose = () => {
    console.log('loginSocket connection closed.');
  };
  navAlarmSocket.onclose = () => {
    console.log('alarmSocket connection closed.');
  };
};
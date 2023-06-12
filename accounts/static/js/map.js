var mapContainer = document.getElementById('map')
var mapOption = {
    center: new kakao.maps.LatLng(33.450701, 126.570667),
    level: 8
}
var map = new kakao.maps.Map(mapContainer, mapOption)

// 마커를 표시할 위치와 title 객체 배열입니다 
var positions = [];

// 지도를 재설정할 범위정보를 가지고 있을 LatLngBounds 객체를 생성합니다
var bounds = new kakao.maps.LatLngBounds(); 

// 주소로 좌표를 검색하고 맵을 업데이트하는 함수
function updateMap(addr) {

    var geocoder = new kakao.maps.services.Geocoder()
    geocoder.addressSearch(addr, function(result, status) {
        if (status === kakao.maps.services.Status.OK) {
            var submitButton = document.getElementById('submit_button');
            submitButton.disabled = true;
            var coords = new kakao.maps.LatLng(result[0].y, result[0].x)
            // Append the object to the positions array
            positions[1] = ({ title: '입력한 주소지', latlng: coords });

            displayMarkers();
        }
    });
}

// HTML5의 geolocation으로 사용할 수 있는지 확인합니다 
if (navigator.geolocation) {
    
    // GeoLocation을 이용해서 접속 위치를 얻어옵니다
    navigator.geolocation.getCurrentPosition(
        function(position) {
            var lat = position.coords.latitude, // 위도
                lon = position.coords.longitude; // 경도
            
            var locPosition = new kakao.maps.LatLng(lat, lon), // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
                message = '<div style="width:150px;text-align:center;padding:6px 0;">현재 위치</div>'; // 인포윈도우에 표시될 내용입니다
            // Append the object to the positions array
            positions[0] = ({ title: '현재 위치', latlng: locPosition });
            displayMarkers();
    
            // Set the center of the map to positions[0]
            var center = locPosition
            map.setCenter(center);
        },
        function(error) {
            mapContainer.style.display = "none";

            var locPosition = new kakao.maps.LatLng(0, 0)
            
            // Append the object to the positions array
            positions[0] = ({ title: '현재 위치 사용 불가', latlng: locPosition });
            displayMarkers();

            // Set the center of the map to positions[0]
            var center = locPosition
            map.setCenter(center);
        }
    );
};

// 마커 이미지의 이미지 주소입니다
var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
    
// Function to display the markers on the map
function displayMarkers() {
    var map = new kakao.maps.Map(mapContainer, mapOption)
    
    for (var i = 0; i < positions.length; i++) {
          
        // 마커 이미지의 이미지 크기 입니다
        var imageSize = new kakao.maps.Size(24, 35);

        // 마커 이미지를 생성합니다
        var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

        // 마커를 생성합니다
        var marker = new kakao.maps.Marker({
            map: map, // 마커를 표시할 지도
            position: positions[i].latlng, // 마커를 표시할 위치
            title: positions[i].title, // 마커의 타이틀, 마커에 마우스를 올리면 타이틀이 표시됩니다
            image: markerImage // 마커 이미지
        });

        // Create the content for the infowindow
        var lat = positions[i].latlng.getLat();
        var lng = positions[i].latlng.getLng();

        var iwContent = '<div style="width:150px;text-align:center;padding:6px 0;">' +
            positions[i].title + '<br>';

        iwContent += '</div>';

        // Create the infowindow
        var infowindow = new kakao.maps.InfoWindow({
            position: positions[i].latlng,
            content: iwContent
        });

        // Open the infowindow on the marker
        infowindow.open(map, marker);

        // Set the center of the map to positions[0]
        var center = positions[0].latlng;
        map.setCenter(center);

        // Example usage
        var lat1 = positions[0].latlng.getLat();
        var lon1 = positions[0].latlng.getLng();
        var lat2 = positions[1].latlng.getLat();
        var lon2 = positions[1].latlng.getLng();

        var distance = calculateDistance(lat1, lon1, lat2, lon2);
        console.log('Distance between the two points: ' + distance + ' kilometers');
        console.log(positions)
        function showDialog(message) {
          var dialog = document.getElementById('dialog');
          var dialogMessage = document.getElementById('dialog-message');
          dialogMessage.innerText = message;
        
          dialog.classList.remove('hidden');
        
          setTimeout(function() {
            dialog.classList.add('hidden');
          }, 1000); // 2초 후에 다이얼로그 숨김
        }
        
        setTimeout(function(distance) {
          if (positions[0].latlng.La === 0 && positions[0].latlng.Ma === 0) {
            var submitButton = document.getElementById('submit_button');
            submitButton.disabled = true;
            showDialog('현재 위치가 확인되지 않습니다');
          } else if (distance > 5) {
            var submitButton = document.getElementById('submit_button');
            submitButton.disabled = true;
            showDialog('입력한 주소지와 현재 위치가 너무 멀어요!');
          } else {
            var submitButton = document.getElementById('submit_button');
            submitButton.disabled = false;
            showDialog('인증되었습니다!');
            
          }
        }, 2000, distance);
        
    }
}

// Function to calculate the distance between two points using Haversine formula
function calculateDistance(lat1, lon1, lat2, lon2) {
    const earthRadius = 6371; // Radius of the Earth in kilometers
    const dLat = (lat2 - lat1) * (Math.PI / 180);
    const dLon = (lon2 - lon1) * (Math.PI / 180);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * (Math.PI / 180)) *
            Math.cos(lat2 * (Math.PI / 180)) *
            Math.sin(dLon / 2) *
            Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = earthRadius * c;
    return distance;
};

// Call the displayMarkers function once to show the initial markers
displayMarkers();
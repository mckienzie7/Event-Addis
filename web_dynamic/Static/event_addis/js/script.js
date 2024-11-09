let map;

const loadMap = function (postion) {
  const { latitude } = postion.coords;
  const { longitude } = postion.coords;
  console.log(
    `https://www.google.com/maps/@${latitude},${longitude}?entry=ttu`
  );

  const coords = [latitude, longitude];
  map = L.map('map').setView(coords, 17);

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);
};

navigator.geolocation.getCurrentPosition(loadMap.bind(this), function () {
  alert('Geolocation is not supported by this browser.');
});

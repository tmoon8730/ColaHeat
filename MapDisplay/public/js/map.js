var map, heatmap;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: 34.000471, lng: -81.041786},
    mapTypeId: 'satellite'
  });

  heatmapPositive = new google.maps.visualization.HeatmapLayer({
    data: getPointPositive(),
    map: map
  });
  heatmapNegative = new google.maps.visualization.HeatmapLayer({
    data: getPointNegative(),
    map: map
  });
  var gradient = [
  'rgba(0, 255, 255, 0)',
  'rgba(0, 255, 255, 1)',
  'rgba(0, 191, 255, 1)',
  'rgba(0, 127, 255, 1)',
  'rgba(0, 63, 255, 1)',
  'rgba(0, 0, 255, 1)',
  'rgba(0, 0, 223, 1)',
  'rgba(0, 0, 191, 1)',
  'rgba(0, 0, 159, 1)',
  'rgba(0, 0, 127, 1)',
  'rgba(63, 0, 91, 1)',
  'rgba(127, 0, 63, 1)',
  'rgba(191, 0, 31, 1)',
  'rgba(255, 0, 0, 1)'
  ]
  heatmapNegative.set('gradient', heatmapNegative.get('gradient') ? null : gradient);
}

// Heatmap data: Positive
function getPointPositive() {
  return [
    new google.maps.LatLng(34.000471, -81.041786),
  ];
}
// Heatmap data: Negative
function getPointNegative() {
  return [
    new google.maps.LatLng(34.000141, -81.041776),
  ];
}

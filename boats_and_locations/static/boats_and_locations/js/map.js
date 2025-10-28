// static/js/mapbox.js

mapboxgl.accessToken = 'pk.eyJ1Ijoiam9obnJqYWNvYnNlbiIsImEiOiJjbHh4bTJmN2Iybm9uMmtwemhzMzJoa3M4In0.nlYJ6TO17TmLHXqui7X1Yw';

document.addEventListener("DOMContentLoaded", function () {
  const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/johnrjacobsen/cm2jhmf0c005x01pebzhw6kf7',
    center: [-80.290833, 34.488448],
    zoom: 7
  });

  // Add popup behavior when clicking on a location
  map.on('click', (event) => {
    const features = map.queryRenderedFeatures(event.point, {
      layers: ['locations_6-27-24'] // Replace with your layer name
    });
    if (!features.length) return;
    const feature = features[0];
    new mapboxgl.Popup({ offset: [0, -15] })
      .setLngLat(feature.geometry.coordinates)
      .setHTML(
        `<h3>${feature.properties.Marina}</h3>
         <p>${feature.properties.Address}</p>
         <a href="${feature.properties.url}" target="_blank" title="Opens in a new window">Flyover</a>`
      )
      .addTo(map);
  });
});

document.addEventListener("DOMContentLoaded", function () {
    var map = L.map('map').setView([38.7223, -9.1393], 12); // Default to Lisbon

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Load the GeoJSON file with train lines
    fetch('/data/metro_lines.json')  // Adjust path if needed
        .then(response => response.json())
        .then(geojson => {
            // Use L.geoJSON to add the GeoJSON data to the map
            L.geoJSON(geojson, {
                onEachFeature: function (feature, layer) {
                    // Add popup with line name
                    if (feature.properties && feature.properties.name) {
                        layer.bindPopup("<b>" + feature.properties.name + "</b>");
                    }
                },
                style: function (feature) {
                    // Check if the color property exists and apply it
                    var lineColor = feature.properties && feature.properties.color ? feature.properties.color : "gray";
                    return {
                        color: lineColor,  // Use the color from GeoJSON properties
                        weight: 5           // Line weight (thickness)
                    };
                }
            }).addTo(map);
        })
        .catch(error => console.error("Error loading GeoJSON:", error));

    // Dummy stations (if needed)
    let dummyStations = [
        { name: "Station A", lat: 38.7169, lon: -9.1399 },
        { name: "Station B", lat: 38.7269, lon: -9.1499 },
        { name: "Station C", lat: 38.7369, lon: -9.1299 }
    ];

    dummyStations.forEach(station => {
        L.marker([station.lat, station.lon])
            .addTo(map)
            .bindPopup(`<b>${station.name}</b>`);
    });
});

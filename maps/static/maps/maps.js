// Define LV95
var lv95 = {
    epsg: "EPSG:2056",
    def: "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs",
    resolutions: [
        8192, 4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2,
        1, 0.5, 0.25, 0.125, 0.0625,
    ],
    origin: [2420000, 1350000],
};

var crs = new L.Proj.CRS(lv95.epsg, lv95.def, {
    resolutions: lv95.resolutions,
    origin: lv95.origin,
});
var map = new L.Map("mapid", {
    crs: crs,
    maxZoom: 15,
    minZoom: 9
}).setView(
    L.CRS.EPSG2056.unproject(L.point(2718572.19, 1200165.34)),
    13
);

const url =
    "https://wms.geo.admin.ch/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities";
const mapOptions = {
    layers: "ch.swisstopo.pixelkarte-farbe",
};
const wmsLayer = L.tileLayer.wms(url, mapOptions).addTo(map);

var markers = [
    { point: L.point(2718572.19, 1200165.34), popup: "Nöldeke" },
    {
        point: L.point(2719254.18, 1200724.44),
        popup: "Schwettiberg-<br>Lädeli",
    },
];

markers.forEach(function (marker, index) {
    var leafletMarker = L.marker(crs.unproject(marker.point))
        .bindPopup(marker.popup)
        .addTo(map);

    if (index == 0) {
        leafletMarker.openPopup();
    }
});

// Get reference to the dropdown
var layerSelector = document.getElementById('layerSelector');

// Store the current layer
var currentLayer;

// Store hike information globally
var hikeInfoData = {};

// Fetch hike information once when the page loads
fetch(hikeInfoUrl)
    .then(response => response.json())
    .then(data => {
        hikeInfoData = data;
    })
    .catch(error => console.error('Error loading hike info:', error));

function toggleHikeInfo(display) {
    var hikeInfo = document.getElementById('hikeInfo');
    hikeInfo.style.display = display ? 'block' : 'none';
}

function displayHikeInfo(path) {
    var info = hikeInfoData[path];
    Object.keys(info).forEach(key => {
        var element = document.getElementById(key);
        if (element) {
            element.textContent = info[key];
        }
    });
    toggleHikeInfo(true);  // Show hike information
    return info.url;
}

function loadGPXLayer(url, map) {
    if (currentLayer) {
        map.removeLayer(currentLayer);
    }

    currentLayer = new L.GPX(url, {
        async: true,
        gpx_options: {
            parseElements: ['track', 'route']  // Only parse tracks and routes
        },
        marker_options: {
            startIconUrl: '',
            endIconUrl: '',
            shadowUrl: '',
            wptIcons: {}
        }
    }).on('loaded', function(e) {
        map.fitBounds(e.target.getBounds());
    }).addTo(map);
}

layerSelector.addEventListener('change', function() {
    var path = this.value;  // Get the selected value
    var layerUrl = displayHikeInfo(path);

    if (layerUrl) {
        loadGPXLayer(staticUrl + layerUrl, map);
    }
});

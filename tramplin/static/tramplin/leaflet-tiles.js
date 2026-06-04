/** Общий слой тайлов для всех карт Трамплин (стабильнее старого *.tile.openstreetmap.org). */
window.TRAMPLIN_addTileLayer = function (map) {
  if (!map || typeof L === "undefined") return null;
  return L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
      subdomains: "abcd",
      maxZoom: 20,
    }
  ).addTo(map);
};

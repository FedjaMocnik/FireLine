import React, { useState } from 'react';
import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, useMapEvents, Marker, Popup } from 'react-leaflet';
import styled from 'styled-components';
import L from 'leaflet';

const MapWrapper = styled.div`
  background-color: #256b68;
  padding: 10px;
  border-radius: 5px;
  max-width: 800px;
  margin: 10px auto;
  height: 500px;
  width: 100%;
  overflow: visible;
`;

const ResultsContainer = styled.div`
  padding: 15px;
  background: #256b68;
  border-radius: 8px;
  max-width: 800px;
  margin: 15px auto;
  color: #FBFAE4;
`;

function ClickHandler({ onMapClick }) {
  useMapEvents({
    click(e) {
      onMapClick(e.latlng);
    }
  });
  return null;
}

function Map({ onCoordsChange }) {
  const [clickedCoords, setClickedCoords] = useState(null);

  const handleMapClick = (coords) => {
    setClickedCoords(coords);
    if (onCoordsChange) {
      onCoordsChange({
        northWest: coords,
        southEast: coords,
        center: coords
      });
    }
  };

  return (
    <div>
      <MapWrapper>
        <MapContainer
          center={[46.0569, 14.5058]}
          zoom={7}
          scrollWheelZoom={true}
          style={{ height: '100%', width: '100%', zIndex:0}}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <ClickHandler onMapClick={handleMapClick} />
          {clickedCoords && (
            <Marker position={clickedCoords}>
              <Popup>
                Lat: {clickedCoords.lat.toFixed(4)}, Lng: {clickedCoords.lng.toFixed(4)}
              </Popup>
            </Marker>
          )}
        </MapContainer>
      </MapWrapper>
      {clickedCoords && (
        <ResultsContainer>
          <h3 style={{ marginBottom: '12px' }}>Koordinate izbrane točke</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px' }}>
            <div>
              <strong>Lat:</strong> {clickedCoords.lat.toFixed(4)} <br />
              <strong>Lng:</strong> {clickedCoords.lng.toFixed(4)}
            </div>
          </div>
        </ResultsContainer>
      )}
    </div>
  );
}

export default Map;
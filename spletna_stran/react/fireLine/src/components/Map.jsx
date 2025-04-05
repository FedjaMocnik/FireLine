//reqirements:npm install leaflet react-leaflet
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import styled from 'styled-components';
import React from 'react';



const MapWrapper = styled.div`
  background-color: rgba(0, 0, 0, 0.5);  /* Black with 50% opacity */
  padding: 10px;
  border-radius: 8px;  /* Rounded corners */
  max-width: 800px;  /* Set a max-width if needed */
  margin: 10px auto;  /* Center the box */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  /* Add some subtle shadow for a better effect */
  height: 500px;  /* Set height to ensure the map fits inside the wrapper */
  width: 100%; /* Ensure full width within the parent container */
`;


function Map() {
  return (
      <MapWrapper>
        <MapContainer 
            center={[46.0569, 14.5058]} 
            zoom={13} 
            scrollWheelZoom={true} 
            style={{ height: "100%", width: "100%" }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Marker position={[46.0569, 14.5058]}>
            <Popup>
              This is a sample marker. You can add wildfire info here.
            </Popup>
          </Marker>
        </MapContainer>
      </MapWrapper>
  );
}

export default Map;
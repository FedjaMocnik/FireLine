/* to kar je komentirano je za rectangle, ce bi sluacjno se kej rabil */

/*import React, { useState, useEffect, useRef, useCallback } from 'react';
import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, useMap, FeatureGroup } from 'react-leaflet';
import styled from 'styled-components';
import L from 'leaflet';
import 'leaflet-draw/dist/leaflet.draw.css';
import 'leaflet-draw';*/

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

  /* .leaflet-draw-draw-rectangle {
    z-index: 1000 !important; */
  }
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

//function Map({ onRectangleChange }) {
  /*const [rectangleCoords, setRectangleCoords] = useState(null);
  const [area, setArea] = useState(null);
  const featureGroupRef = useRef(new L.FeatureGroup());

  const handleDrawCreate = useCallback((e) => {
    featureGroupRef.current.clearLayers();
    if (e.layerType === 'rectangle') {
      const layer = e.layer;
      
      layer.setStyle({
        color: '#2ecc71',
        weight: 2,
        fillOpacity: 0.3,
        fillColor: '#2ecc71'
      });
      
      featureGroupRef.current.addLayer(layer);
      
      const bounds = layer.getBounds();
      const area = L.GeometryUtil.geodesicArea(bounds);
      setArea(area / 1000000);
      
      const coords = {
        northWest: bounds.getNorthWest(),
        southEast: bounds.getSouthEast(),
        center: bounds.getCenter()
      };
  
      setRectangleCoords(coords);
      
      if (onRectangleChange) {
        onRectangleChange(coords);
      }
  
      layer.bindPopup(`
        <div style="font-weight: bold; color: #2c3e50;">
          Click the edit tool to modify
        </div>
      `);
    }
  }, [onRectangleChange]);

  const handleDrawEdited = useCallback((e) => {
    const layers = e.layers;
    layers.eachLayer((layer) => {
      const bounds = layer.getBounds();
      const area = L.GeometryUtil.geodesicArea(bounds);
      
      setArea(area / 1000000);
      
      const coords = {
        northWest: bounds.getNorthWest(),
        southEast: bounds.getSouthEast(),
        center: bounds.getCenter()
      };
      
      setRectangleCoords(coords);
      
      if (onRectangleChange) {
        onRectangleChange(coords);
      }

      layer.bindPopup(`
        <div style="font-weight: bold; color: #2c3e50;">
          Click the edit tool to modify
        </div>
      `);
    });
  }, [onRectangleChange]);

  function DrawingTools() {
    const map = useMap();

    useEffect(() => {
      if (!map || !L.Draw) return;

      // Add feature group to map
      featureGroupRef.current.addTo(map);

      // Initialize draw control
      const drawControl = new L.Control.Draw({
        position: 'topright',
        draw: {
          polygon: false,
          polyline: false,
          circle: false,
          circlemarker: false,
          marker: false,
          rectangle: {
            shapeOptions: {
              color: '#3388ff',
              weight: 3,
              fillOpacity: 0.3,
              fillColor: '#3388ff',
              dashArray: '5,5'
            },
            showArea: false
          }
        },
        edit: {
          featureGroup: featureGroupRef.current,
          edit: {
            selectedPathOptions: {
              color: '#e74c3c',
              fillColor: '#e74c3c'
            }
          }
        }
      });

      map.addControl(drawControl);

      map.on(L.Draw.Event.CREATED, handleDrawCreate);
      map.on(L.Draw.Event.EDITED, handleDrawEdited);

      return () => {
        map.off(L.Draw.Event.CREATED, handleDrawCreate);
        map.off(L.Draw.Event.EDITED, handleDrawEdited);
        map.removeControl(drawControl);
        map.removeLayer(featureGroupRef.current);
      };
    }, [map, handleDrawCreate, handleDrawEdited]);

    return null;
  }*/

  function Map() {
    const [clickedCoords, setClickedCoords] = useState(null);

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
          <ClickHandler onMapClick={setClickedCoords} />
          {clickedCoords && (
            <Marker position={clickedCoords}>
              <Popup>
                Lat: {clickedCoords.lat.toFixed(4)}, Lng: {clickedCoords.lng.toFixed(4)}
              </Popup>
            </Marker>
          )}
          {/*} <DrawingTools /> */}
        </MapContainer>
      </MapWrapper>
      {clickedCoords && ( //prej rectangle
        <ResultsContainer>
          <h3 style={{ marginBottom: '12px' }}>Koordinate izbrane točke</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px' }}>
            <div>
              <strong>Lat:</strong> {clickedCoords.lat.toFixed(4)} <br />
              <strong>Lng:</strong> {clickedCoords.lng.toFixed(4)}
            </div>
            {/*<div>
              <strong>Zgornji desni kot:</strong><br />
              {rectangleCoords.northWest.lat.toFixed(4)}, {rectangleCoords.northWest.lng.toFixed(4)}
            </div>
            <div>
              <strong>Spodnji levi kot:</strong><br />
              {rectangleCoords.southEast.lat.toFixed(4)}, {rectangleCoords.southEast.lng.toFixed(4)}
            </div>
            <div>
              <strong>Sredina:</strong><br />
              {rectangleCoords.center.lat.toFixed(4)}, {rectangleCoords.center.lng.toFixed(4)}
            </div>*/}
          </div>
        </ResultsContainer>
      )}
    </div>
  );
}

export default Map;
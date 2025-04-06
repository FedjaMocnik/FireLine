import React, { useState, useEffect, useRef } from 'react';
import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, Marker, Popup, useMap, FeatureGroup } from 'react-leaflet';
import styled from 'styled-components';
import L from 'leaflet';
import 'leaflet-draw/dist/leaflet.draw.css';
import 'leaflet-draw';

const MapWrapper = styled.div`
  background-color: #256b68;
  padding: 10px;
  border-radius: 8px;
  max-width: 800px;
  margin: 10px auto;
  height: 500px;
  width: 100%;
  overflow: visible;

  .leaflet-draw-draw-rectangle {
    z-index: 1000 !important;
  }
`;

const ResultsContainer = styled.div`
  padding: 15px;
  background: #256b68;
  border-radius: 8px;
  max-width: 800px;
  margin: 15px auto;
  color: white;
`;

function Map() {
  const [rectangleCoords, setRectangleCoords] = useState(null);
  const [area, setArea] = useState(null);
  const featureGroupRef = useRef(new L.FeatureGroup());

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

      function handleDrawCreate(e) {
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
          
          setRectangleCoords({
            northWest: bounds.getNorthWest(),
            southEast: bounds.getSouthEast(),
            center: bounds.getCenter()
          });

          layer.bindPopup(`
            <div style="font-weight: bold; color: #2c3e50;">
              Click the edit tool to modify
            </div>
          `);
        }
      }

      // Handler for editing existing rectangles
      function handleDrawEdited(e) {
        const layers = e.layers;
        layers.eachLayer((layer) => {
          // After editing, get the new bounds
          const bounds = layer.getBounds();
          const area = L.GeometryUtil.geodesicArea(bounds);

          // Update the coordinates and area after editing
          setArea(area / 1000000); // Convert area to square km
          setRectangleCoords({
            northWest: bounds.getNorthWest(),
            southEast: bounds.getSouthEast(),
            center: bounds.getCenter(),
          });

          // Optionally, update the popup with new info
          layer.bindPopup(`
            <div style="font-weight: bold; color: #2c3e50;">
              Click the edit tool to modify
            </div>
          `);
        });
      }

      map.on(L.Draw.Event.CREATED, handleDrawCreate);
      map.on(L.Draw.Event.EDITED, handleDrawEdited);

      return () => {
        map.off(L.Draw.Event.CREATED, handleDrawCreate);
        map.off(L.Draw.Event.EDITED, handleDrawEdited);
        map.removeControl(drawControl);
        map.removeLayer(featureGroupRef.current);
      };
    }, [map]);

    return null;
  }

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
          <DrawingTools />
        </MapContainer>
      </MapWrapper>
      {rectangleCoords && (
        <ResultsContainer>
          <h3 style={{ color: 'white', marginBottom: '12px' }}>Koordinate izbranega območja</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px' }}>
            <div>
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
            </div>
          </div>
        </ResultsContainer>
      )}
      </div>
  );
}

export default Map;
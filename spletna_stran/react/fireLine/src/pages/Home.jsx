import styled from 'styled-components';
import React, { useState } from 'react';
import Map from '../components/Map'; 
import GenerateButton from '../components/GenerateButton';

const HomeWrapper = styled.div`
  background-color: rgba(13, 37, 32, 1.0);  
  color: white;  
  padding: 20px;
  border-radius: 8px;
  width: 1000px;  
  margin: 30px auto;
`;

function Home() {
  const [rectangleCoords, setRectangleCoords] = useState(null);

  return (
    <HomeWrapper>
      <h1>FireLine: preprečevanje gozdnih požarov</h1>
      <h2>Zemljevid</h2>
      <p>Izberi območje</p>
      <Map onRectangleChange={setRectangleCoords} />
      <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
        <GenerateButton rectangleCoords={rectangleCoords} />
      </div>
    </HomeWrapper>
  );
}

export default Home;
import styled from 'styled-components';
import React, { useState } from 'react';
import Map from '../components/Map'; 
import GenerateButton from '../components/GenerateButton';
import DateInput from '../components/DateInput';

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
  const [date, setDate] = useState(() => new Date().toISOString().split('T')[0]);

  return (
    <HomeWrapper>
      <h1>FireLine: preprečevanje gozdnih požarov</h1>
      <h2>Orodje</h2>
      <p style={{ margin: '20px'}} >1. Izberi točko začetka požara:</p>
      <Map onCoordsChange={setRectangleCoords} /> 

      <div>
        <DateInput selectedDate={date} onDateChange={setDate} />
      </div>
      <div className="flex items-center justify-center bg-gray-100 p-4">
        <GenerateButton 
          rectangleCoords={rectangleCoords} 
          selectedDate={date}  
        />
      </div>
    </HomeWrapper>
  );
}

export default Home;
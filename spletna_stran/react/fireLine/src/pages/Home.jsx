import styled from 'styled-components';
import React from 'react';
import Map from '../components/Map'; 
import ImageCard from '../components/ImageCard'; 
import GenerateButton from '../components/GenerateButton';

const HomeWrapper = styled.div`
  background-color: rgba(13, 37, 32, 1.0);  
  color: white;  
  padding: 20px;
  border-radius: 8px;
  width: 1000px;  
  margin: 30px auto;  /* Center the box */
`;


function Home() {
  return (
    <HomeWrapper>
      <h1>FireLine: preprečevanje goznih požarov</h1>
      <h2>Zemljevid</h2>
      <p>Izberi območje</p>
      <Map/>
        <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <GenerateButton/>
      </div>
    </HomeWrapper>
  );
}

export default Home;
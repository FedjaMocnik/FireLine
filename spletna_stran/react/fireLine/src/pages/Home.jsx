import styled from 'styled-components';
import React from 'react';
import Map from '../components/Map'; 
import ImageCard from '../components/ImageCard'; 
import GenerateButton from '../components/GenerateButton';

const HomeWrapper = styled.div`
  background-color: rgba(0, 0, 0, 0.5);  /* Black with 50% opacity */
  color: white;  /* Text color */
  padding: 15px;
  border-radius: 8px;  /* Rounded corners */
  width: 900px;  /* Set a max-width if needed */
  margin: 30px auto;  /* Center the box */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  /* Add some subtle shadow for a better effect *
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
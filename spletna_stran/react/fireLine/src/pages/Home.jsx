import styled from 'styled-components';
import React from 'react';
import Map from '../components/Map'; 

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
    </HomeWrapper>
  );
}

export default Home;
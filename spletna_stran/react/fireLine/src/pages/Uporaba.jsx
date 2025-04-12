import React from 'react';
import styled from "styled-components";


const UporabaWrapper = styled.div`
  background-color: rgba(13, 37, 32, 1.0);  
  color: white; 
  padding: 20px;
  border-radius: 8px;  
  width: 1000px;  
  margin: 30px auto;  /* Center the box */

`;


function Uporaba() {
  return (
    <UporabaWrapper>
      <h1>Navodila za uporabo orodja FireLine</h1>
      <p>neki neki neki</p>
    </UporabaWrapper>
  );
}

export default Uporaba;


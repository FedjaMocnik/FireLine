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
      <p>1. Na zemljevidu s klikom izberete točko, kjer se je požar začel.</p>
      <p>2. V koledarju izberete datum začetka požara. Privzeti datum je današnji.</p>
      <p>3. Zaženete orodje FireLine s klikom na gumb: ZAŽENI FIRELINE.</p>
      <p>Obdelava podatkov in ustvarjanje rezultatov lahko traja nekaj minut.</p>
    </UporabaWrapper>
  );
}

export default Uporaba;


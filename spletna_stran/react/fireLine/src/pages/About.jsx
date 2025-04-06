import React from 'react';
import styled from "styled-components";


const AboutWrapper = styled.div`
  background-color: rgba(13, 37, 32, 0.8);  /*  80% opacity */
  color: white;  /* Text color */
  padding: 15px;
  border-radius: 8px;  /* Rounded corners */
  width: 900px;  
  margin: 30px auto;  /* Center the box */

`;


function About() {
  return (
    <AboutWrapper>
      <h1>FireLine</h1>
      <h2>Napovedovanje širjenja gozdnih požarov in preprečevanje katastrofalnih posledic</h2>
      <p>Podnebne spremembe povečujejo pogostost in intenzivnost gozdnih požarov, kar povzroča ogromno škodo ekosistemom in naseljem. FireLine je inovativna rešitev, ki omogoča napovedovanje širjenja požarov ter strateško postavljanje požarnih pregrad za zmanjšanje tveganja in zaščito okolja.</p>
      <p>Sistem temelji na analizi satelitskih podatkov (Copernicus, OpenMeteo), ki zajemajo vegetacijo, vlažnost in vremenske razmere. Na podlagi teh informacij FireLine simulira širjenje požara ter predlaga optimalne požarne pregrade, ki preprečujejo nenadzorovano širitev ognja. Za modeliranje uporabljamo metode semantične segmentacije (AiTLAS) in simulacijske algoritme (Cell2Fire), pri čemer rezultate obdelujemo s pomočjo superračunalnika.</p>
      <p>Aplikacija bo ključna za gasilske organizacije, civilno zaščito in lastnike zemljišč v požarno ogroženih območjih. FireLine podpira cilje trajnostnega razvoja UNESCO, predvsem podnebne ukrepe (SDG 13) in ohranjanje kopenskih ekosistemov (SDG 15), saj pomaga pri varovanju narave in zmanjšanju emisij toplogrednih plinov zaradi požarov.</p>
    </AboutWrapper>
  );
}

export default About;


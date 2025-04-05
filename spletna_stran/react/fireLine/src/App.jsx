import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header'
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import styled from "styled-components";

const AppWrapper = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;  // Ensures that the footer stays at the bottom even with little content
`;

const MainContent = styled.main`
  flex-grow: 1;  // Allows the content area to grow and push footer to bottom
`;

function App() {
    return(
      <Router>
        <AppWrapper>
          <Header />
          <MainContent>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </MainContent>
          <Footer />
        </AppWrapper>
    </Router>
    );
}

export default App;

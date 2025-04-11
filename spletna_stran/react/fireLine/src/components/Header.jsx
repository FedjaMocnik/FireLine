import {Link} from 'react-router-dom'
import styled from "styled-components"; 
// Styled components for styling
const HeaderWrapper = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #256b68;
  position: sticky;
  top: 0;
  z-index: 100;
  padding-left: 40px;
  padding-right: 60px; 
`;

const LogoLink = styled(Link)`
  display: flex;
  align-items: center;
  text-decoration: none;
  transition: transform 0.2s ease-in-out; /* This makes the scaling smooth */
  
  &:hover {
    transform: scale(1.025);

    span {
    color: #f39c12;
  }
  }
`;

const LogoImage = styled.img`
  height: 70px;
  width: auto;
  margin-right: 10px;

`;

const LogoText = styled.span`
  color: #B0E7E6;
  font-size: 1.8rem;
  font-weight: bold;

`;

const Navbar = styled.nav`
  a {
    margin: 0 15px;
    color: #B0E7E6;
    text-decoration: none;
    font-weight: 600;
    transition: transform 0.2s ease-in-out; 
    display: inline-block; /* Ensure the 'a' tag is treated as a block to allow scaling */
  }

  a:hover {
    color: #f39c12;
    transform: scale(1.05);
  }
`;



function Header() {
    
    return(
        <HeaderWrapper>
            <LogoLink to="/">
                <LogoImage src="/logoFireLine.png" alt="Logo" />
                <LogoText>FireLine</LogoText>
            </LogoLink>
            <Navbar>
              <Link to="/">Domov/zemljevid</Link>
              <Link to="/about">O projektu</Link>
            </Navbar>
    </HeaderWrapper>
    );
}

export default Header
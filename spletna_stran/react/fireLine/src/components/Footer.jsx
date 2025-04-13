import styled from "styled-components";

// Styled component for the footer
const FooterWrapper = styled.footer`
  background-color: #256b68;
  color: white;
  padding: 20px;
  text-align: center;
  position: relative;
  bottom: 0;
  width: 100%;
  font-size: 1rem;
`;

const Footer = () => {
  return (
    <FooterWrapper>
      <p>2025 FireLine - 5 prijateljev</p>
    </FooterWrapper>
  );
};

export default Footer;
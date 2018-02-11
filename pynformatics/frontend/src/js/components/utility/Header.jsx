import React from 'react';
import styled from 'styled-components';

import IsoPageHeader from '../../isomorphic/components/utility/pageHeader';

const HeaderWrapper = styled.div`
  > * { 
    margin-left: 0;
    margin-bottom: 20px; 
  }
`;

const Header = (props) => (
  <HeaderWrapper style={props.style}>
    <IsoPageHeader {...props} />
  </HeaderWrapper>
);

export default Header;

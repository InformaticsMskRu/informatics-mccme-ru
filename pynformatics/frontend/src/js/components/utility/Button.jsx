import styled from 'styled-components';

import IsoButton from '../../isomorphic/components/uielements/button';


const Button = styled(IsoButton)`
  &.ant-btn {
    border-radius: 4px;
    
    &.ant-btn-primary {
      background-color: rgb(64, 126, 255);
    }
  }
`;

export default Button;

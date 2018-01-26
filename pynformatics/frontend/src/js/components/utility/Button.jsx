import styled from 'styled-components';
import { palette } from 'styled-theme';

import IsoButton from '../../isomorphic/components/uielements/button';


const Button = styled(IsoButton)`
  &.ant-btn {

    &.ant-btn-secondary {
      color: #ffffff;
      background: ${palette('other', 2)};
      border-color:  ${palette('other', 2)};
    }
  }
`;

export default Button;

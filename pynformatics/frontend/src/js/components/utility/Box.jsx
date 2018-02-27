import React from 'react';
import styled from 'styled-components';
import { palette } from 'styled-theme';

import { BoxWrapper as IsoBoxWrapper } from '../../isomorphic/components/utility/box.style';
import {
  BoxTitle as IsoBoxTitleWrapper,
  BoxSubTitle as IsoBoxSubTitleWrapper
} from '../../isomorphic/components/utility/boxTitle.style';


const BoxWrapper = IsoBoxWrapper.extend`
  border-radius: 4px;
  color: ${palette("other", 7)};
  
  &&& {
    margin: 0;
  }
`;

const BoxTitleWrapper = IsoBoxTitleWrapper.extend`
  font-size: 22px;
  margin-right: 10px;
  display: inline-block;
  margin-bottom: 0;
  color: ${palette("other", 7)};
`;

const BoxSubTitleWrapper = IsoBoxSubTitleWrapper.extend`
  font-size: 14px;
  display: inline-block;
  margin-bottom: 0;
`;

const BoxHeaderWrapper = styled.div`
  margin-bottom: 20px;
`;

const BoxHeader = ({title, subtitle}) => (
  <BoxHeaderWrapper>
    { title ? <BoxTitleWrapper>{' '}{title}{' '}</BoxTitleWrapper> : '' }
    { subtitle ? <BoxSubTitleWrapper>{' '}{subtitle}{' '}</BoxSubTitleWrapper>: '' }
  </BoxHeaderWrapper>
);

const Box = ({ title, subtitle, children, style, className }) => (
  <BoxWrapper style={style} className={className}>
    { title || subtitle ? <BoxHeader title={title} subtitle={subtitle}/> : null }
    { children }
  </BoxWrapper>
);

export default Box;

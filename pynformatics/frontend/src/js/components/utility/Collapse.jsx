import React from 'react';
import styled from 'styled-components';

import IsoCollapses from '../../isomorphic/components/uielements/collapse';
import IsoCollapseWrapper from '../../isomorphic/containers/Uielements/Collapse/collapse.style';


// TODO: эти стили завязаны на главной странице, вынести то, что относится только к ней
const CollapseWrapper = styled(IsoCollapseWrapper)`
  background: #ffffff;
  
  && > .ant-collapse > .ant-collapse-item > .ant-collapse-header {
    background: #ffffff;
    padding: 0;
    height: auto;
  }
  
  .ant-collapse-content {
    padding-left: 0;
    padding-right: 0;
    
    .ant-collapse-content-box {
      padding-bottom: 0;
    }
  }
  
`;

const Collapse = props => (
  <CollapseWrapper>
    <IsoCollapses {...props}>{props.children}</IsoCollapses>
  </CollapseWrapper>
);

const Panel = IsoCollapses.Panel;


export default Collapse;
export { Panel };

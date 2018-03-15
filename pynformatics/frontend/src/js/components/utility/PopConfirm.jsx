import React from 'react';
import styled, { injectGlobal } from 'styled-components';

import {
    rowStyle,
    Row,
} from '../../components/utility/Grid';

import Button from './Button'
import Tooltip from './Tooltip';


injectGlobal`
  .PopConfirmWrapper {
    .ant-tooltip-arrow { display: none; }
    .ant-tooltip-inner {
      background: #FFFFFF;
      padding: 20px;
      max-width: 300px;
      border-radius: 6px;
      box-shadow: 0 0 24px 0 rgba(182, 189, 197, 0.42);
    }
  }
`;

const PopConfirmTitleWrapper = styled.div`
  font-size: 14px;
  color: #343a40;
`;

const PopConfirmTitle = ({title}) => (
  <PopConfirmTitleWrapper>{title}</PopConfirmTitleWrapper>
);

export default class PopConfirm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {visible: false};
    this.closeFunction = this.closeFunction.bind(this);
  }
  closeFunction = (func) => {
    this.setState({...this.state, visible: false});
    func();
  };
  render() {
    return (
      <Tooltip
        trigger="onclick"
        placement={this.props.placement}
        overlayClassName="PopConfirmWrapper"
        visible={this.state.visible}
        onVisibleChange = {() => this.setState({...this.state, visible: !this.state.visible})}
        title={
          <div>
            <Row style={{...rowStyle, marginBottom: '20px'}}>
              <PopConfirmTitle title={this.props.title}/>
            </Row>
            <Row style={rowStyle}>
              <Button type="primary" size="small"
                      onClick={() => {this.closeFunction(this.props.onConfirm)}} style={{marginRight: '15px'}}>
                {this.props.okText}
              </Button>
              <Button type="primary" size="small"
                      onClick={() => {this.closeFunction(this.props.onCancel)}}>
                {this.props.cancelText}
              </Button>
            </Row>
          </div>
        }
      >
        {this.props.children}
      </Tooltip>
    );
  }
}

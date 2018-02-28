import { palette } from 'styled-theme';
import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import * as _ from 'lodash';
import Clipboard from 'clipboard';


import Button from '../../components/utility/Button';
import {
  colStyle,
  gutter,
  rowStyle,
  Col,
  Row,
} from '../../components/utility/Grid';
import { borderRadius } from '../../isomorphic/config/style-util';


const SampleWrapper = styled.div`
  color: ${palette('other', 7)};
  
  .block {
    background: #F8F8F8;
    padding: 10px;
    ${borderRadius('4px')}
    height: 100%;
    width: 100%;
  }
  
  .header {
    display: flex;
    height: 36px;
    margin-bottom: 4px;
    
    > * { margin: auto 0; }
    .copyBtn { margin-left: auto;  }
  }
  
  pre {
    text-align: left;
    counter-reset: line;
  
    span {
      display: block;
      color: #393A39;
      font-size: 13px;
      font-family: 'PT mono', monospace;
      font-weight: bold;
      
      &:before {
        display: inline-block;
        margin-right: 5px;
        opacity: 0.5;
        font-weight: normal;
        
        counter-increment: line;
        content: counter(line);
      }
    }
  }
  
`;

export class Sample extends React.Component {
  static propTypes = {
    input: PropTypes.string,
    correct: PropTypes.string,
  };

  static wrapLines(text) {
    const lines = text.split('\n');
    if (lines[lines.length - 1] === '') {
      lines.pop();
    }
    return {
      maxLength: _.isEmpty(lines) ? 0 : _.maxBy(lines, line => line.length).length,
      lines: _.map(lines, (line, index) => (
        <span key={index}>{line}</span>
      )),
    };
  }

  static inlineMaxCharacters = 32;

  componentDidMount() {
    new Clipboard('.copyBtn');
  }

  render() {
    const { input, correct } = this.props;

    const { maxLength: maxInput, lines: wrappedInput } = Sample.wrapLines(input);
    const { maxLength: maxCorrect, lines: wrappedCorrect } = Sample.wrapLines(correct);

    const inline = (maxInput <= Sample.inlineMaxCharacters && maxCorrect < Sample.inlineMaxCharacters);

    return (
      <SampleWrapper>
        <Row style={rowStyle} gutter={gutter}>
          <Col md={inline ? 12 : 24} xs={24} style={colStyle}>
            <div className="block">
              <div className="header">
                <div>Входные данные</div>
                <Button
                  className="copyBtn"
                  type="secondary"
                  data-clipboard-text={input}
                >Копировать</Button>
              </div>
              <pre className="input">
                {wrappedInput}
              </pre>
            </div>
          </Col>
          <Col md={inline ? 12 : 24} xs={24} style={colStyle}>
            <div className="block">
              <div className="header">
                <div>Выходные данные</div>
              </div>
              <pre className="correct">
                {wrappedCorrect}
              </pre>
            </div>
          </Col>
        </Row>
      </SampleWrapper>
    )
  }
}

export default Sample;
export { SampleWrapper }

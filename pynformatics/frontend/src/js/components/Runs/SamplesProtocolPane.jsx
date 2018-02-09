import { palette } from 'styled-theme'
import React from 'react';

import Sample, { SampleWrapper } from '../Problem/Sample';
import { Row, Col, rowStyle, colStyle, gutter } from '../../components/utility/Grid';


const SamplesProtocolWrapper = SampleWrapper.extend`
  .samplesRow:not(:last-child) {
    margin-bottom: 30px;
  }

  .samplesHeader {
    font-size: 16px;
    font-weight: 500;
    color: ${palette('other', 7)};
  }
`;


export default ({samples}) => {
  const sampleBlocks = _.map(samples, (value, key) => {
    const wrapped = _.mapValues(_.pick(value, ['input', 'corr', 'output', 'error_output']),
        text => Sample.wrapLines(text));
    const maxLength = _.maxBy(_.map(_.pick(wrapped, ['input', 'corr'])),
        value => value.maxLength).maxLength;

    const inlineMaxCharacter = 37;

    return (
      <Row className="samplesRow" key={key} style={rowStyle} gutter={gutter}>
        <Col xs={24} style={colStyle}>
          <div className="samplesHeader">Тест №{key}</div>
        </Col>
        <Col md={maxLength <= inlineMaxCharacter ? 12 : 24} xs={24} style={colStyle}>
          <div className="block">
            <div className="header">Входные данные</div>
            <pre>{ wrapped['input'].lines }</pre>
          </div>
        </Col>
        <Col md={maxLength <= inlineMaxCharacter ? 12 : 24} xs={24} style={colStyle}>
          <div className="block">
            <div className="header">Правильный ответ</div>
            <pre>{ wrapped['corr'].lines }</pre>
          </div>
        </Col>
        <Col xs={24} style={colStyle}>
          <div className="block">
            <div className="header">Вывод программы</div>
            <pre>{ wrapped['output'].lines }</pre>
          </div>
        </Col>
        {
          wrapped['error_output'].maxLength > 0
          ? (
            <Col xs={24} style={colStyle}>
              <div className="block">
                <div className="header">Поток вывода ошибок</div>
                <pre>{ wrapped['error_output'].lines }</pre>
              </div>
            </Col>
          ) : null
        }
      </Row>
    )
  });
  return (
    <SamplesProtocolWrapper>
      {sampleBlocks}
    </SamplesProtocolWrapper>
  );
}
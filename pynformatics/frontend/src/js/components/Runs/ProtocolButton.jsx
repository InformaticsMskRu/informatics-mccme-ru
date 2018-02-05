import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import React from 'react';
import { Table } from 'antd';
import * as _ from 'lodash';


import Button from '../utility/Button';
import CodeMirror from '../../components/utility/CodeMirror';
import Modal from '../utility/Modal';
import Status from './Status';
import Tabs, { TabPane } from '../utility/Tabs';
import * as problemActions from '../../actions/problemActions';
import SamplesProtocolPane from './SamplesProtocolPane';


export class ProtocolButton extends React.Component {
  static propTypes = {
    problemId: PropTypes.number.isRequired,
    runId: PropTypes.number.isRequired,
    contestId: PropTypes.number.isRequired,
    problems: PropTypes.object.isRequired,
  };

  constructor() {
    super();

    this.state = {
      visible: false,
    };

    this.showModal = this.showModal.bind(this);
  }

  showModal() {

    const { problemId, runId, contestId, dispatch } = this.props;
    dispatch(problemActions.fetchProblemRunProtocol(problemId, contestId, runId));

    this.setState({...this.state, visible: true});
  }

  render() {
    const { problemId, runId, problems } = this.props;
    const run = _.get(problems, `[${problemId}].runs[${runId}]`, {});

    const {
      tests,
      compiler_output: compilerOutput,
    } = run.protocol || {};

    const testsColumns = [
      {
        dataIndex: 'key',
        key: 'key',
        title: '#'
      },
      {
        dataIndex: 'status',
        key: 'status',
        title: 'Статус',
        render: status => <Status status={status}/>
      },
      {
        dataIndex: 'time',
        key: 'time',
        title: 'Время работы',
      },
      {
        dataIndex: 'realTime',
        key: 'realTime',
        title: 'Астрономическое время работы',
      },
      {
        dataIndex: 'maxMemoryUsed',
        key: 'maxMemoryUsed',
        title: 'Используемая память'
      },
    ];
    const testsData = _.map(tests, (value, key) => ({
      key,
      status: value.status,
      time: (value.time / 1000).toFixed(3),
      realTime: (value.real_time / 1000).toFixed(3),
      maxMemoryUsed: value.max_memory_used,
    }));

    const samples = _.pickBy(tests, test => _.has(test, 'input'));

    return (
      <div>
        <Modal
          visible={this.state.visible}
          footer={null}
          mask={false}
          onCancel={() => this.setState({...this.state, visible: false})}
          width={720}
          destroyOnClose={true}
        >
          <Tabs>
            <TabPane key="source" tab="Код">
              <CodeMirror
                value={'# Просмотр кода пока не реализован'}
                options={{
                  lineNumbers: true,
                  readOnly: true,
                  tabSize: 4,
                  mode: 'text-x/python',
                }}
              />
            </TabPane>
            <TabPane key="protocol" tab="Протокол">
              <Table
                dataSource={testsData}
                columns={testsColumns}
                size="small"
                pagination={false}
              />
              { compilerOutput
                ? (
                  <div className="compilerOutput">
                    <div>Сообщение компилятора:</div>
                    <div>{compilerOutput}</div>
                  </div>
                )
                : null
              }
            </TabPane>
            <TabPane key="samplesProtocol" tab="Тесты из условия">
              <SamplesProtocolPane samples={samples}/>
            </TabPane>
            {/*<TabPane key="fullProtocol" tab="Полный протокол">1</TabPane>*/}
          </Tabs>
        </Modal>
        <Button
          type="secondary"
          size="small"
          style={{ padding: 0, display: 'flex' }}
          onClick={this.showModal}
        >
          <i className="material-icons">keyboard_arrow_right</i>
        </Button>
      </div>
    );
  }
}

export default connect(state => ({
  problems: state.problems,
}))(ProtocolButton);

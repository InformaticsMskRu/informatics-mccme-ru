import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Table } from 'antd';
import { connect } from 'react-redux';
import * as _ from 'lodash';

import ProblemCell from './ProblemCell';
import ProblemColumnHeader from './ProblemColumnHeader';
import { processStandingsData } from '../../utils/standings';


const columnsBeforeProblems = [
  {
    title: '#',
    dataIndex: 'rowNumber',
    key: 'rowNumber',
    className: 'standingsTableRowNumberColumn',
  },
  {
    title: 'Участник',
    dataIndex: 'user',
    key: 'user',
    className: 'standingsTableUserColumn'
  },
];

const columnsAfterProblems = [
  {
    title: 'Всего',
    dataIndex: 'total',
    key: 'total',
    className: 'standingsTableTotalColumn'
  },
  {
    title: 'Попыток',
    dataIndex: 'attempts',
    key: 'attempts',
    className: 'standingsTableAttemptsColumn'
  },
];


const StandingsTableWrapper = styled.div`
  .ant-table-content { overflow-x: auto; }

  .standingsTableRowNumberColumn {
    white-space: nowrap;
    width: 1px;
  }

  .standingsTableUserColumn {
    white-space: nowrap;
  }

  .standingsTableProblemColumn, 
  .standingsTableTotalColumn, 
  .standingsTableAttemptsColumn {
    text-align: center;
    white-space: nowrap;
    width: 1px;

    &.highlighted {
      background: red;
    }
  }
`;

export class StandingsTable extends React.Component {
  static contextTypes = {
    statementId: PropTypes.number,
  };
  
  static propTypes = {
    statements: PropTypes.object.isRequired,
  };

  constructor(props, context) {
    super(props, context);

    this.state = {
      highlight: null,
    }
    this.initProblemColumns();

    this.initProblemColumns = this.initProblemColumns.bind(this);

    processStandingsData();
  }

  initProblemColumns() {
    const { statementId } = this.context;
    this.singleProblem = typeof statementId === 'undefined';

    if (this.singleProblem) {
      this.columnsProblems = [
        {
          title: 'Результат',
          dataIndex: 'problem',
          key: 'problem',
          className: 'standingsTableProblemColumn',
          render: ({score, time_created: time, attempts}) => <ProblemCell score={score} time={time} attempts={attempts} shrinkable={false} />,
        }
      ];
      this.defaults = {problem: {}};
    } else {
      const statement = this.props.statements[statementId];
      if (!statement) {
        this.columnsProblems = [];
      } else {
        this.columnsProblems = _.map(statement.problems, (problem, rank) => ({
          title: <ProblemColumnHeader rank={rank} title={problem.name} />,
          dataIndex: problem.id,
          key: problem.id,
          className: 'standingsTableProblemColumn' + (this.state.highlight === problem.id ? 'highlighted' : ''),
          render: ({score, time_created: time, attempts}) => <ProblemCell score={score} time={time} attempts={attempts} />,
          onCell: () => ({
            onMouseEnter: () => this.setState({...this.state, highlight: problem.id}),
            onMouseLeave: () => this.setState({...this.state, highlight: null})
          })
        }));
        this.defaults = {};
        _.forEach(statement.problems, problem => this.defaults[problem.id] = {});
      }
    }
  }

  render() {
    let tempData = _.sortBy(_.map(processStandingsData(), (data, userId) => ({
      key: userId,
      user: data.first_name + ' ' + data.last_name,
      ...this.defaults,
      ...data.processed.summary,
      ...data.processed.problems,
    })), [value => -value.total, value => value.attempts]);
    tempData = _.map(tempData, (value, index) => ({...value, rowNumber: index + 1}));

    const columns = this.singleProblem 
      ? _.concat(columnsBeforeProblems, this.columnsProblems) 
      : _.concat(columnsBeforeProblems, this.columnsProblems, columnsAfterProblems)

    return (
      <StandingsTableWrapper>
        <Table
          bordered
          columns={columns}
          dataSource={tempData}
          pagination={false}
        />
      </StandingsTableWrapper>
    );
  }
}

export default connect(state => ({
  statements: state.statements,
})
)(StandingsTable);

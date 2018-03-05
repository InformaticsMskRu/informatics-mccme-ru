import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Table } from 'antd'
import { connect } from 'react-redux';
import { palette } from 'styled-theme';
import * as _ from 'lodash';

import Button from '../../components/utility/Button';
import ProtocolButton from './ProtocolButton';
import Status from './Status';
import moment from '../../utils/moment';
import { LANGUAGES } from '../../constants';
import * as problemActions from '../../actions/problemActions';


const RunsWrapper = styled.div`
  .ant-table-thead > tr > th {
    background: ${palette('other', 15)};
    color: rgba(33, 37, 41,0.5);
    font-weight: normal;
    font-size: 12px;
  }
  .ant-table-content { overflow-x: auto; }

  .runsColumnScore,
  .refreshBtn {
    width: 1px;
    text-align: center;
    white-space: nowrap;
  }
  .runsColumnId,
  .runsColumnStatus,
  .runsColumnDate,
  .runsColumnLanguage {
    text-align: center;
    white-space: nowrap;
  }
  
  .buttons {
    display: flex;
    flex-flow: row wrap;
    justify-content: space-between;
    margin-top: 10px;
    
    @media (max-width: 767px) { display: none; }
  }
  
  .refreshBtn {
    i { cursor: pointer; }
    span { display: flex; }
  }
`;

export class Runs extends React.Component {
  static contextTypes = {
    statementId: PropTypes.number,
  };

  static propTypes = {
    problemId: PropTypes.number.isRequired,
    runs: PropTypes.object.isRequired,
    showUserInfo: PropTypes.bool,
    showRows: PropTypes.number,

    windowWidth: PropTypes.number.isRequired,
  };

  static defaultProps = {
    showUserInfo: false,
    showRows: 5,
  };

  constructor() {
    super();

    this.state = {
      showMore: false,
    };

    this.fetchProblemRuns = this.fetchProblemRuns.bind(this);
    this.toggleShowMore = this.toggleShowMore.bind(this);
  }

  fetchProblemRuns() {
    const { statementId } = this.context;
    const { problemId } = this.props;
    this.fetchProblemRunsPromise = this.props.dispatch(
      problemActions.fetchProblemRuns(problemId, statementId)
    );
  }

  toggleShowMore() {
    this.setState({
      ...this.state,
      showMore: !this.state.showMore,
    })
  }

  render() {
    const { showMore } = this.state;
    const {
      problemId,
      showRows,
      showUserInfo,
      windowWidth,
      user,
    } = this.props;

    const columns = [
      {
        dataIndex: 'status',
        key: 'status',
        render: status => <Status status={status}/>,
        className: 'runsColumnStatus',
      },
      {
        dataIndex: 'id',
        key: 'id',
        title: '#',
        className: 'runsColumnId',
      },
      {
        dataIndex: 'time',
        key: 'time',
        title: 'Дата',
        className: 'runsColumnDate',
      },
      {
        dataIndex: 'language',
        key: 'language',
        title: 'Язык',
        className: 'runsColumnLanguage',
      },
      {
        dataIndex: 'score',
        key: 'score',
        title: 'Баллы',
        className: 'runsColumnScore',
      },
      {
        className: 'refreshBtn',
        key: 'refresh',
        title: (
          <i
            onClick={this.fetchProblemRuns}
            className="material-icons"
          >
            sync
          </i>
        ),
        render: run => (
          <ProtocolButton
            problemId={run.problemId}
            runId={run.id}
            contestId={run.contestId}
          />
        ),
      },
    ];

    if (showUserInfo) {
      columns.splice(2, 0, {
        dataIndex: 'user',
        key: 'user',
        title: 'Участник'
      });
    }

    const data = _.sortBy(_.map(this.props.runs, (value, key) => ({
      key,
      problemId,
      contestId: parseInt(value.contest_id),
      id: parseInt(key),
      status: value.status,
      time: value.create_time 
        ? moment(value.create_time).calendar(null, {
          sameDay: 'HH:mm',
          lastDay: '[Вчера в] HH:mm',
          lastWeek: 'DD.MM.YYYY HH:mm',
          sameElse: 'DD.MM.YYYY HH:mm',
        }) : '',
      language: LANGUAGES[value.lang_id].name || '',
      score: value.score,
      user: (
        value.user
          ? value.user.firstname + ' ' + value.user.lastname
          : user.firstname + ' ' + user.lastname
      )
    })), row => -row.id);

    return (
      <RunsWrapper>
        <Table
          columns={columns}
          dataSource={ showMore || windowWidth < 768 ? data : data.slice(0, showRows) }
          pagination={false}
          scroll={{ x: 600 }}
        />
        <div className="buttons">
          <Button
            type="secondary"
            onClick={this.toggleShowMore}
            disabled={data.length <= showRows}
          >
            Показать еще
          </Button>
          <Button type="secondary" disabled>Архив посылок</Button>
        </div>
      </RunsWrapper>
    );
  }
}

export default connect(state => ({
  user: state.user,
  windowWidth: state.ui.width,
}))(Runs);

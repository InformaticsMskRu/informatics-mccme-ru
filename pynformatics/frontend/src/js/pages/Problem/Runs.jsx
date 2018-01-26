import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';
import { Table } from 'antd'
import * as _ from 'lodash';
import { palette } from 'styled-theme';
import { connect } from 'react-redux';

import { LANGUAGES, STATUSES } from '../../constants';
import Button from '../../components/utility/Button';
import Status from './Status';
import * as problemActions from '../../actions/problemActions';


const RunsWrapper = styled.div`
  .ant-table-thead > tr > th {
    background: #F3F5F7;
    color: rgba(33, 37, 41,0.5);
    font-weight: normal;
    font-size: 12px;
  }
  
  .ant-table { 
    border-radius: 0;
    color: ${palette('other', 7)}; 
  }
  .ant-table table { border-radius: 0; }
  
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
  static propTypes = {
    problemId: PropTypes.number.isRequired,
    runs: PropTypes.object.isRequired,
    windowWidth: PropTypes.number.isRequired,
  };

  static showRows = 5;

  constructor() {
    super();

    this.state = {
      showMore: false,
    };

    this.fetchProblemRunsPromise = null;

    this.fetchProblemRuns = this.fetchProblemRuns.bind(this);
    this.toggleShowMore = this.toggleShowMore.bind(this);
  }

  fetchProblemRuns() {
    const { problemId } = this.props;
    if (!this.fetchProblemRunsPromise) {
      this.fetchProblemRunsPromise = this.props.dispatch(
        problemActions.fetchProblemRuns(problemId)).then(() => {
          this.fetchProblemRunsPromise = null;
        });
    }
  }

  toggleShowMore() {
    this.setState({
      ...this.state,
      showMore: !this.state.showMore,
    })
  }

  render() {
    const { showMore } = this.state;
    const { windowWidth } = this.props;

    const columns = [
      {
        dataIndex: 'status',
        key: 'status',
        title: '',
        render: status => <Status status={status}/>,
      },
      {
        dataIndex: 'id',
        key: 'id',
        title: '#',
      },
      {
        dataIndex: 'time',
        key: 'time',
        title: 'Дата',
      },
      {
        dataIndex: 'language',
        key: 'language',
        title: 'Язык',
      },
      {
        dataIndex: 'score',
        key: 'score',
        title: 'Баллы',
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
        render: () => (
          <Button type="secondary" size="small" style={{ padding: 0, display: 'flex' }}>
            <i className="material-icons">keyboard_arrow_right</i>
          </Button>
        ),
      },
    ];

    const data = _.sortBy(_.map(this.props.runs, (value, key) => ({
      key,
      id: key,
      status: value.status,
      time: value.create_time || '',
      language: LANGUAGES[value.lang_id].name || '',
      score: value.score,
    })), row => -row.id);


    return (
      <RunsWrapper>
        <Table
          columns={columns}
          dataSource={ showMore || windowWidth < 768 ? data : data.slice(0, Runs.showRows) }
          pagination={false}
          scroll={{ x: 600 }}
        />
        <div className="buttons">
          <Button onClick={this.toggleShowMore} type="secondary">Показать еще</Button>
          <Button type="secondary">Архив посылок</Button>
        </div>
      </RunsWrapper>
    );
  }
}

export default connect(state => ({
  windowWidth: state.ui.width,
}))(Runs);

import React from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom'

import * as problemRequestsListActions from '../../actions/problemRequestsListActions';
import MainContentWrapper from "../utility/MainContentWrapper";

import Box from '../../components/utility/Box';
import {List} from 'antd';


@connect(state => ({
  problemRequests: state.problemRequestsList,
}))
export default class ProblemRequestsList extends React.Component {
  constructor(props) {
    super(props);
    this.fetchList();
  }

  fetchList() {
    this.props.dispatch(problemRequestsListActions.fetchRequestsList());
  }

  render() {
    const data = this.props.problemRequests;

    if (!data) {
      return <MainContentWrapper>
        <div>data not found</div>
      </MainContentWrapper>
    }

    return (
      <MainContentWrapper>
        <Box style={{height: 'auto', width: 'auto'}}>
          <List
            header={<div><h3>Список отредактированных задач</h3></div>}
            bordered
            dataSource={Object.keys(data).reverse().map((i)  => data[i])}
            renderItem={item => (
              <List.Item>
                <List.Item.Meta
                  title={
                    <Link to={`/problem_request/${item.id}`}>
                      {`${item.id} Статус: ${item.status}`}
                    </Link>
                  }
                  description={`Номер: ${item.problem.id} Название: ${item.problem.name}`}
                />
              </List.Item>
            )}
          />
        </Box>
      </MainContentWrapper>
    );
  }
}
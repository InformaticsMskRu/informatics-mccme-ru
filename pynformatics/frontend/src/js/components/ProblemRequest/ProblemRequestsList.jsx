import React from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom'

import * as problemRequestsListActions from '../../actions/problemRequestsListActions';
import MainContentWrapper from "../utility/MainContentWrapper";

import Box from '../../components/utility/Box';
import {List} from 'antd';

@connect(state => ({
  problem_requests: state.problem_requests_list,
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
    const data = this.props.problem_requests;

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
            dataSource={Object.keys(data).map((i)  => data[i])}
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
/*
<div>
  <ul>
    {Object.keys(data).map((i)  =>
      <li key={i}>
        id: {data[i].id},
        status: {data[i].status},
        problem: {data[i].problem.id} {data[i].problem.name},
        link: {<Link to={`/problem_request/${data[i].id}`}> Ссылка</Link>}
      </li>
    )}
  </ul>
</div>
*/

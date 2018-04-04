import React from 'react';
import { Spin } from 'antd';
import { withRouter } from 'react-router-dom';

import axios from '../../utils/axios';
import MainContentWrapper from '../../components/utility/MainContentWrapper';


export class GroupInvite extends React.Component {
  constructor(props) {
    super(props);
    
    const { groupInviteUrl } = props.match.params;
    axios.post(`/group/join/${groupInviteUrl}`, {}, {camelcaseKeys: true})
      .then(response => {
        const { 
          joined, 
          redirect: { courseId, statementId } 
        } = response.data;

        if (joined) console.log('joined');

        if (statementId) {
          props.history.push(`/contest/${statementId}`);
        }
      })
  }

  render() {
    return (
      <MainContentWrapper style={{ display: 'flex', alignContent: 'center', justifyContent: 'center' }}>
          <Spin size="large" style={{ margin: '20% auto' }} />
      </MainContentWrapper>
    );
  }
}

export default withRouter(GroupInvite);

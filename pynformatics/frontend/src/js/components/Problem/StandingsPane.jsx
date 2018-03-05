import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import * as _ from 'lodash';

import GroupFilter from '../GroupFilter/GroupFilter';
import StandingsTable from '../StandingsTable/StandingsTable';



export class StandingsPane extends React.Component {
  static propTypes = {
    problemId: PropTypes.number.isRequired,
    filterGroup: PropTypes.object,
  };

  render() {
    const { problemId, filterGroup } = this.props;
    const filterGroupId = _.get(filterGroup, 'id');

    return (
      <div>
        <GroupFilter style={{ marginBottom: 16 }} />
        <StandingsTable problemId={problemId} filterGroupId={filterGroupId} />
      </div>
    );
  }
}


export default connect(state => ({
  filterGroup: state.group.filterGroup,
}))(StandingsPane);

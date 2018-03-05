import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { connect } from 'react-redux';
import * as _ from 'lodash';

import Button from '../utility/Button';
import Select, { SelectOption } from '../utility/Select';
import AutoComplete from '../utility/AutoComplete';
import { InputGroup } from '../utility/Input';
import { createGroupSelect } from '../GroupSelect/GroupSelect';
import * as groupActions from '../../actions/groupActions';


const GroupSelect = createGroupSelect('groupFilter');


const GroupFilterWrapper = styled.div`
  display: flex;
  flex-flow: row nowrap;

  .groupFilterSelect {
    flex: 1;
    margin: auto 8px auto 0;
    max-width: 350px;
  }

  .groupFilterButton {
    margin: auto 0;
  }
`;


export class GroupFilter extends React.Component {
  static propTypes = {
    filterGroup: PropTypes.object,
    search: PropTypes.object,
  }

  constructor(props) {
    super(props);

    this.state = {
      forFilter: props.filterGroup,
    }

    this.unsetGroupFilter = this.unsetGroupFilter.bind(this);
    this.setGroupFilter = this.setGroupFilter.bind(this);
  }

  unsetGroupFilter() {
    this.props.dispatch(groupActions.setGroupFilter());
  }

  setGroupFilter() {
    this.props.dispatch(groupActions.setGroupFilter(this.state.forFilter));
  }

  render() {
    const { filterGroup, style } = this.props;
    const { forFilter } = this.state;
    const { id: groupId, name: groupName } = forFilter || {};

    return (
      <GroupFilterWrapper style={style}>
        <GroupSelect
          allowClear={true}
          className="groupFilterSelect"
          onChange={(name) => {
            if (filterGroup && name !== filterGroup.name) {
              this.setState({...this.state, forFilter: undefined});
              this.unsetGroupFilter();
            }
          }}
          onSelect={(name, selectOption) => this.setState({
            ...this.state,
            forFilter: {
              id: parseInt(selectOption.props.groupId),
              name: selectOption.props.groupName,
            }
          })}
          defaultValue={groupId && groupName 
            ? `${groupId} - ${groupName}`
            : undefined
          }
          dropdownMatchSelectWidth={false}
        />
        <Button
          type="primary"
          disabled={!forFilter}
          onClick={this.setGroupFilter}
        >
          Применить
        </Button>
      </GroupFilterWrapper>
    );
  }
}

export default connect(state => ({
  filterGroup: state.group.filterGroup,
}))(GroupFilter);

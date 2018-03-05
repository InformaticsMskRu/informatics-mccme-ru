import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import * as _ from 'lodash';

import Select, { SelectOption } from '../utility/Select';
import * as groupActions from '../../actions/groupActions';


const defaultSearchUID = 'groupSelect'


class GroupSelect extends React.Component {
  static propTypes = {
    searchUID: PropTypes.string.isRequired,
    search: PropTypes.object,
  };

  constructor(props) {
    super(props);

    const { searchUID } = props;

    this.searchGroups = this.searchGroups.bind(this, searchUID);
  }

  componentDidMount() {
    this.searchGroups('');
  }

  searchGroups(searchUID, name) {
    this.props.dispatch(groupActions.searchGroup(name, searchUID));
  }

  render() {
    const { search, onChange, ...rest } = this.props;
    const data = _.map(search, (group, id) => (
      <SelectOption 
        key={id} 
        value={`${id} - ${group.name}`} 
        groupId={id}
        groupName={group.name}
      >
        {group.name}
      </SelectOption>
    ));

    return (
      <Select
        mode="combobox"
        filterOption={false}
        // optionLabelProp="name"
        placeholder="Название группы"
        notFoundContent="Группы не найдены"
        onChange={typeof onChange === 'undefined'
          ? this.searchGroups
          : (value) => {
            this.searchGroups(value);
            onChange(value)
          }
        }
        {...rest}
      >
        {data}
      </Select>
    );
  }
}


export const createGroupSelect = (searchUID) => connect(state => ({
  searchUID: searchUID,
  search: _.get(state.group.search, `[${searchUID}]`),
}))(GroupSelect)


export default createGroupSelect(defaultSearchUID);

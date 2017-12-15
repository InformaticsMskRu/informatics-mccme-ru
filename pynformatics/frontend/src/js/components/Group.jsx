import React from 'react';
import * as groupActions from '../actions/groupActions';
import {connect} from 'react-redux';

@connect(state => ({
    groups: state.groups,
}))
export default class Group extends React.Component {

    constructor(props) {
        super(props);
        this.groupId = parseInt(this.props.match.params.groupId, 10);
        this.fetchGroup();
    }

    fetchGroup() {
        this.props.dispatch(groupActions.fetchGroup(this.groupId));
    }

    render() {
        const group = this.props.groups[this.groupId];
        if (!group || group && group.fetching) {
            return <div>Fetching...</div>
        }

        if (!group.fetched) {
            return <div>Some error</div>
        }

        const {data} = group;
        return (
            <div>
                <h1>Name: {data.name}</h1>
                <h3>Description:</h3> {data.description}
                <h3>Owner:</h3> {data.owner.firstname} {data.owner.lastname}
                <h3>Users:</h3>
                <ul>{data.users.map((user, i) => <li key={i}>{user.firstname} {user.lastname}</li>)}</ul>
            </div>
        );
    }
}

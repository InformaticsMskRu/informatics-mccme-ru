import React from 'react';
import { connect } from 'react-redux';

import * as userdataActions from '../actions/userdataActions';


@connect(state => ({
        userdata: state.userdata,
}))
export default class Userdata extends React.Component {
    constructor(props) {
        super(props);
        this.userId = parseInt(this.props.match.params.userId, 10);
        console.log("constr", this.userId);
        this.fetchUserdata(this.userId);
    }

    fetchUserdata(userId) {
        this.props.dispatch(userdataActions.fetchUserdata(userId));
    }

    render() {
        const data = this.props.userdata[this.userId];

        console.log("!! componenta ", data);

        if (!data) {
            return <div> user data not found </div>
        }

        return (
            <div>
                <h1> Name: {data.firstname} {data.lastname} </h1>
                <h3> Email: {data.email} </h3>
                <h3>Groups:</h3>
                <ul>
                    {data.groups.name.map((name, i) =>
                        <li key={i}> {name} </li>
                    )}
                </ul>

            </div>
            /*<h1>Name: {data.firstname} {data.lastname}</h1>
                <h3>Email:</h3> {data.email}
                <h3>Groups:</h3>
                /*<ul>
                    {data.map((groups) =>
                    <li key={groups}>
                        id: {groups.group_id}, name: {groups.name}
                    </li>)}
                </ul>*/
        );
    }
}

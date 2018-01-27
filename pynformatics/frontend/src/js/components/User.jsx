import React from 'react';
import { connect } from 'react-redux';

import * as userActions from '../actions/userActions';


@connect(state => ({
        user: state.user,
}))
export default class User extends React.Component {
    constructor(props) {
        super(props);
        this.userId = parseInt(this.props.match.params.userId, 10);
        console.log("constr", this.userId);
        this.fetchUser(this.userId);
    }

    fetchUser(userId) {
        this.props.dispatch(userActions.fetchUser(userId));
    }

    render() {
        const data = this.props.user[this.userId];

        console.log("!! componenta ", data);

        if (!data) {
            return <div> user data not found </div>
        }

        return (
            <div>
                <h1>Name: {data.firstname} {data.lastname}</h1>
                <h3>Email:</h3> {data.email}
                <h3>Groups:</h3>
                <ul>
                    {Object.keys(data.groups).map(id =>
                    <li key={id}>
                        id: {id}, name: {data.groups[id]}
                    </li>
                    )}
                </ul>
            </div>
            /*
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
            */
        );
    }
}

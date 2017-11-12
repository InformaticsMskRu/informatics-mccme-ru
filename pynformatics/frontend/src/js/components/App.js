import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

import Statement from './Statement';


export default class App extends React.Component {
    render() {
        return <div>
            <div class="main-content">
                <Switch>
                    <Route path="/statement/:statementId/problem/:problemRank" component={Statement}/>
                    <Route path="/statement/:statementId" render={({ match }) => (
                        <Redirect to={`/statement/${match.params.statementId}/problem/1`}/>
                    )}/>
                </Switch>
            </div>
        </div>
    }
}
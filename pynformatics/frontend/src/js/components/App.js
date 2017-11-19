import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

import Statement from './Statement';
import StatementAdmin from '../pages/StatementAdmin';


export default class App extends React.Component {
    render() {
        return <div>
            <div class="main-content">
                <Switch>
                    <Route exact path="/statement/:statementId" component={Statement}/>
                    <Route exact path="/statement/:statementId/problem/:problemRank" component={Statement}/>
                    <Route exact path="/admin/statement/:statementId" component={StatementAdmin}/>
                </Switch>
            </div>
        </div>
    }
}
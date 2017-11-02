import React from 'react';
import { Switch, Route } from 'react-router-dom';

import Statement from './Statement';


export default class App extends React.Component {
    render() {
        return <div>
            <div class="main-content">
                <Switch>
                    <Route path="/statement/:statementId" component={Statement}/>
                </Switch>
            </div>
        </div>
    }
}
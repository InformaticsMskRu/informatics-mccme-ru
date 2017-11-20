import React from 'react';
import { Switch, Route } from 'react-router-dom';

import Statement from './Statement';
import StatementAdmin from '../pages/StatementAdmin';


export default function App() {
  return (
    <div>
      <div className="main-content">
        <Switch>
          <Route exact path="/statement/:statementId" component={Statement} />
          <Route exact path="/statement/:statementId/problem/:problemRank" component={Statement} />
          <Route exact path="/admin/statement/:statementId" component={StatementAdmin} />
        </Switch>
      </div>
    </div>
  );
}
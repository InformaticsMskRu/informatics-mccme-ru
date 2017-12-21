import React from 'react';
import { connect } from 'react-redux';
import { reduxForm, Field, formValueSelector, getFormMeta, initialize } from 'redux-form';
import { withRouter } from 'react-router-dom';

import * as statementActions from '../actions/statementActions';
import { LANGUAGES } from '../constants';


const formName = 'statementSettings';
const valueSelector = formValueSelector(formName);
const metaSelector = getFormMeta(formName);

@reduxForm({
  form: formName,
})
@connect((state) => {
  return {
    statements: state.statements,
    formMeta: metaSelector(state),
    formValues: valueSelector(state, 'allowed_languages', 'type'),
  };
})
@withRouter
export default class StatementAdmin extends React.Component {
  componentWillMount() {
    const { statementId } = this.props.match.params;
    this.props.dispatch(statementActions.fetchStatement(statementId)).then(() => {
      const { settings } = this.props.statements[statementId];
      this.props.dispatch(initialize(formName, settings));
    });
  }

  setSettings() {
    const { statementId } = this.props.match.params;
    const { formValues } = this.props;
    this.props.dispatch(statementActions.setSettings(statementId, formValues));
  }

  render() {
    const { handleSubmit } = this.props;
    const { statementId } = this.props.match.params;
    const statement = this.props.statements[statementId];
    if (!statement || !statement.fetched) {
      return <h1>fetching</h1>
    }

    const languagesOptions = _.map(LANGUAGES, (value, key) => {
      return <option key={key} value={key}>{value.name}</option>
    });

    return <div>
      <form onSubmit={handleSubmit(this.setSettings.bind(this))}>
        <div>
          <div><label for="allowed_languages">Allowed languages</label></div>
          <Field
            name="allowed_languages"
            component="select"
            type="select-multiple"
            id="allowed_languages"
            style={{'width': '200px'}}
            size="10"
            multiple
          >
            {languagesOptions}
          </Field>
        </div>
        <div>
          <div><label for="type">Тип контеста</label></div>
          <Field name="type" component="select" id="type" normalize={value => (value === "" ? null : value)}>
            <option value="">Открытый</option>
            <option value="olympiad">Олимпиада</option>
            <option value="virtual">Виртуальный</option>
          </Field>
        </div>
        <div>
          {/*<Field name="submit" component="input" type="submit"/>*/}
          <input type="submit" value="submit"/>
        </div>
      </form>
    </div>
  }
}

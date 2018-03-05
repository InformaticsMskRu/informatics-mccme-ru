import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { reduxForm, Field, getFormMeta, formValueSelector, initialize } from 'redux-form';
import * as _ from 'lodash';

import * as statementActions from '../actions/statementActions';
import { LANGUAGES } from '../constants';

const formName = 'statementSettingsForm';
const formFields = [
  'allowed_languages',
  'freeze_time',
  'group',
  'restrict_view',
  'standings',
  'start_from_scratch',
  'team',
  'test_only_samples',
  'test_until_fail',
  'time_start',
  'time_stop',
  'type',
];
const formConfig = {
  allowed_languages: null,
  freeze_time: {
    type: 'integer',
    label: 'Заморозка',
  },
  group: {
    type: 'integer',
    label: 'Группа',
  },
  restrict_view: {
    type: 'boolean',
    label: 'Restrict view',
  },
  standings: {
    type: 'boolean',
    label: 'Показывать таблицу результатов',
  },
  start_from_scratch: {
    type: 'boolean',
    label: 'Начинать контест с 0',
  },
  team: {
    type: 'boolean',
    label: 'Командный',
  },
  test_only_samples: {
    type: 'boolean',
    label: 'Тестировать только на тестах из условия',
  },
  test_until_fail: {
    type: 'boolean',
    label: 'Тестировать до первой ошибки',
  },
  type: null,
};
const valueSelector = formValueSelector(formName);
const metaSelector = getFormMeta(formName);


@reduxForm({
  form: formName,
})
@connect(state => ({
  statements: state.statements,
  formMeta: metaSelector(state),
  formValues: valueSelector(
    state,
    ...formFields,
  ),
}))
export default class StatementSettingsForm extends React.Component {
  static propTypes = {
    statementId: PropTypes.number.isRequired,
  };

  static getStatementSettings(props) {
    const {statementId} = props;
    return _.get(props, `statements[${statementId}].settings`);
  }

  constructor(props) {
    super(props);

    const {statementId} = props;
    props.dispatch(statementActions.fetchStatement(statementId)).then((res) => {
      console.log(res);
    });

    this.setSettings = this.setSettings.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    const {statementId} = this.props;
    const {statementId: nextStatementId} = nextProps;

    const settings = StatementSettingsForm.getStatementSettings(this.props);
    const nextSettings = StatementSettingsForm.getStatementSettings(nextProps);

    if (statementId !== nextStatementId || !_.isEqual(settings, nextSettings)) {
      this.props.dispatch(initialize(formName, nextSettings));
    }
  }

  setSettings() {
    const {statementId, formValues: settings} = this.props;
    this.props.dispatch(statementActions.setSettings(statementId, settings)).catch((error) => {
      console.log(error);
      alert('Error!');
    });
  }

  render() {
    const {handleSubmit} = this.props;

    const languagesOptions = _.map(LANGUAGES, (value, key) => {
      return <option key={key} value={key}>{value.name}</option>
    });

    const configuredFields = [];
    _.each(formFields, (field) => {
      if (formConfig[field]) {
        const {type, label, ...other} = formConfig[field];
        switch (type) {
          case 'integer':
            other.type = 'text';
            other.normalize = value => parseInt(value, 10);
            break;
          case 'boolean':
            other.type = 'checkbox';
            break;
          default:
            break;
        }
        configuredFields.push(
          <div key={field}>
            <label>
              <div>{label}</div>
              <Field name={field} component="input" type={type} {...other} />
            </label>
          </div>
        );
      }
    });

    return (
      <div>
        <form onSubmit={handleSubmit(this.setSettings)}>
          <div>
            <label>
              <div>Тип контеста</div>
              <Field name="type" component="select" id="type"
                     normalize={value => (value === '' ? null : value)}>
                <option value="">Открытый</option>
                <option value="olympiad">Олимпиада</option>
                <option value="virtual">Виртуальный</option>
              </Field>
            </label>
          </div>

          <div>
            <label>
              <div>Allowed languages</div>
              <Field
                name="allowed_languages"
                component="select"
                type="select-multiple"
                id="allowed_languages"
                style={{width: '200px'}}
                size="10"
                normalize={value => _.map(value, stringId => parseInt(stringId, 10))}
                multiple
              >
                {languagesOptions}
              </Field>
            </label>
          </div>

          {configuredFields}

          <div>
            <input type="submit" value="submit"/>
          </div>
        </form>
      </div>
    );
  }
}
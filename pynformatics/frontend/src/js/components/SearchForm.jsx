import React from "react";
import {connect} from "react-redux";
import {Field, reduxForm, formValueSelector} from 'redux-form'
import PropTypes from "prop-types";
import * as _ from "lodash";

import * as searchActions from '../actions/searchActions'

const formName = 'searchForm';
const valueSelector = formValueSelector(formName);


@reduxForm({
  form: formName,
})
@connect(state => ({
  formValues: {
    query: valueSelector(state, 'query')
  },
  pages_total: state.search.pages_total,
  page: state.search.page,
  fetched: state.search.fetched,
}))
export default class SearchForm extends React.Component {
  static propTypes = {
    dispatch: PropTypes.func,
    handleSubmit: PropTypes.func,
    formValues: PropTypes.any,
    pristine: PropTypes.bool,
    submitting: PropTypes.bool,
    mode: PropTypes.string.isRequired,
    page: PropTypes.number,
    pages_total: PropTypes.number,
    fetched: PropTypes.bool,
  };

  search = (additionalParams = {}) => {
    const {query} = this.props.formValues;
    this.props.dispatch(searchActions.searchUser(query, additionalParams))
      .catch((error) => {
        console.log(error);
      });
  };

  debouncedSearch = _.debounce(() => {
    setTimeout(this.search, 0);
  }, 1000);

  render() {
    const {handleSubmit, submitting, mode, page, pages_total} = this.props;
    const pagesHrefs = _.map(_.range(pages_total + 1), (number) => {
      if (page !== number)
        return <button key={number} onClick={() => this.search({page: number})}>{number}</button>;
      else
        return <span key={number}> {number} </span>;
    });
    let formProps;
    switch (mode) {
      case 'submit':
        formProps = {
          onSubmit: handleSubmit(this.search)
        };
        break;
      case 'live':
        formProps = {
          onChange: this.debouncedSearch,
          onSubmit: handleSubmit(this.debouncedSearch)
        };
        break;
    }
    return (
      <div>
        <form {...formProps}>
          <div>
            <label>Запрос</label>
            <div>
              <Field
                name='query'
                component='input'
                type='text'
                placeholder='Запрос'
              />
            </div>
          </div>
          {mode === 'submit'
            ?
            <div>
              <button type='submit' disabled={submitting}>
                Искать
              </button>
            </div>
            :
            <div></div>
          }
        </form>
        <div>
          {this.props.fetched ? pagesHrefs : 'Loading...'}
        </div>
      </div>
    );
  }
}
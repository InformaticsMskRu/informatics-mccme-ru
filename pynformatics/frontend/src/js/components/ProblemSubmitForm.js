import * as _ from 'lodash';
import React from 'react';
import { connect } from 'react-redux';
import { Field, reduxForm, formValueSelector, getFormMeta, initialize } from 'redux-form';

import * as problem from '../actions/problemActions';
import { LANGUAGES } from '../constants';

import FileInput from '../utils/FileInput';


const formName = 'problemSubmitForm';
const valueSelector = formValueSelector(formName);
const metaSelector = getFormMeta(formName);

@reduxForm({
    form: formName,
})
@connect((state) => ({
    formMeta: metaSelector(state),
    formValues: {
        file: valueSelector(state, 'file'),
        langId: valueSelector(state, 'langId'),
        source: valueSelector(state, 'source'),
    },
}))
export default class ProblemSubmitForm extends React.Component {
    constructor(props) {
        super(props);
        try {
            this.languageInfo = JSON.parse(localStorage.getItem('languageInfo')) || {};
        }
        catch(error) {
            this.languageInfo = {};
        }

        const {problem: {data: {languages}}} = props;
        const lastUsedLanguage = _.maxBy(
            _.keys(languages),
            key => _.get(this.languageInfo[key], 'lastUsed', 0)
        );
        props.dispatch(initialize(formName, {langId: lastUsedLanguage, submit: 'submit'}));
    }

    fileFieldChange(event, newValue, previousValue) {
        const langIdMeta = _.get(this, 'props.formMeta.langId', {});
        if (!newValue.length || langIdMeta.touched)
            return;

        const extension = newValue[0].name.slice(newValue[0].name.lastIndexOf('.'));
        const {accLangId} = _.reduce(
            LANGUAGES,
            ({accLangId, accLangLastUsed}, lang, langId) => {
                const langLastUsed = _.get(this.languageInfo, `${langId}.lastUsed`, 0);
                if (lang.extension !== extension || langLastUsed <= accLangLastUsed)
                    return {accLangId, accLangLastUsed};
                return {
                    accLangId: langId,
                    accLangLastUsed: langLastUsed,
                }
            },
            {
                accLangId: -1,
                accLangLastUsed: -1,
            }
        );
        if (accLangId !== -1)
            this.props.autofill('langId', accLangId);
    }

    submitProblem() {
        const {langId, file, source} = this.props.formValues;

        _.set(this.languageInfo, `${langId}.lastUsed`, Date.now());
        localStorage.setItem('languageInfo', JSON.stringify(this.languageInfo));

        const data = {
            langId,
            source,
            file: file ? file[0] : undefined,
        };
        this.props.dispatch(problem.submitProblem(this.props.problem.data.id, data));
    }

    render() {
        const {handleSubmit, problem: {data: {languages}}} = this.props;
        const options = Object.keys(languages).map(
            langId => (<option key={langId} value={langId}>{languages[langId]}</option>)
        );

        return <div class="problem-submit-form">
            <form onSubmit={handleSubmit(this.submitProblem.bind(this))}>
                <div>
                    <Field component="select" name="langId">
                        {options}
                    </Field>
                </div>
                <div><Field component={FileInput} type="file" name="file" onChange={this.fileFieldChange.bind(this)}/></div>
                <div><Field component="textarea" name="source"/></div>
                <div><Field component="input" type="submit" name="submit" /></div>
            </form>
        </div>
    }
}
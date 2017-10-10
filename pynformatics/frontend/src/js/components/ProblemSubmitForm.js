import React from 'react';
import {connect} from 'react-redux';
import {Field, reduxForm, formValueSelector} from 'redux-form';

import * as problem from '../actions/problemActions';

import FileInput from '../utils/FileInput';


const formName = 'problemSubmitForm';
const selector = formValueSelector(formName);


@connect((state) => ({
    formValues: {
        file: selector(state, 'file'),
        langId: selector(state, 'langId'),
    }
}))
export class ProblemSubmitForm extends React.Component {
    submitProblem() {
        let data = {
            langId: this.props.formValues.langId,
            file: this.props.formValues.file[0],
        };
        this.props.dispatch(problem.submitProblem(this.props.problem.id, data));
    }

    render() {
        const {handleSubmit, problem: {languages}} = this.props;
        const options = Object.keys(languages).map(
            langId => <option key={langId} value={langId}>{languages[langId]}</option>
        );

        return <div class="problem-submit-form">
            <form onSubmit={handleSubmit(this.submitProblem.bind(this))}>
                <div>
                    <Field component="select" name="langId">
                        {options}
                    </Field>
                </div>
                <div><Field component={FileInput} type="file" name="file"/></div>
                <div><Field component="input" type="submit" name="submit" value="submit"/></div>
            </form>
        </div>
    }
}

export default reduxForm({
    form: formName,
})(ProblemSubmitForm);

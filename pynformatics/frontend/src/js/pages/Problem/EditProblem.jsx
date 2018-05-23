import React from 'react';
import * as problemActions from '../../actions/problemActions';
import {connect} from 'react-redux';
import MainContentWrapper from '../../components/utility/MainContentWrapper';
import Button from '../../components/utility/Button';
import styled from 'styled-components';
import Box from '../../components/utility/Box';
import {ProblemStatement} from "./ProblemStatement";
import MonacoEditor from 'react-monaco-editor';
import message from '../../isomorphic/components/feedback/message';

const ProblemWrapper = styled.div`
  > div {
    height: auto;
  }
`;

@connect(state => ({
    problems: state.problems,
}))
export default class EditProblem extends React.Component {

    constructor(props) {
        super(props);
        this.problemId = parseInt(this.props.match.params.problemId, 10);
        this.state = {};
        this.fetchProblem()
    }

    fetchProblem() {
        this.props.dispatch(problemActions.fetchProblem(this.problemId));
    }

    editProblem() {
        this.props.dispatch(problemActions.editProblem(this.state.name, this.state.code, this.problemId))
            .then(() => message.success('Изменения приняты'))
            .catch(error => message.error(error.response.data.message));
    }

    setNewName(name) {
        this.setState({name})
    }

    setNewCode(code) {
        this.setState({code});
    }

    render() {
        const problem = this.props.problems[this.problemId];
        if (!problem || problem && problem.fetching) {
            return <div>Fetching...</div>
        }

        if (!problem.fetched) {
            return <div>Some error</div>
        }

        const {data} = problem;
        if (this.state.name === undefined) {
            this.setNewName(data.name)
        }
        if (this.state.code === undefined) {
            this.setNewCode(data.content)
        }
        return (
            <MainContentWrapper>
                <ProblemWrapper>
                    <Box>
                        <div>Название: <input
                            onChange={event => this.setNewName(event.target.value)} type={'text'}
                            value={this.state.name}/></div>
                        <MonacoEditor
                            height="600"
                            language="html"
                            value={this.state.code}
                            onChange={(newCode) => this.setNewCode(newCode)}
                        />
                        <h3>Предпросмотр:</h3>
                        <ProblemStatement statement={this.state.code}/>
                        <Button
                            onClick={() => this.editProblem()}
                            type="primary"
                            loading={this.props.problems.problemRequest.fetching}>
                            Отправить
                        </Button>
                    </Box>
                </ProblemWrapper>
            </MainContentWrapper>
        );
    }
}

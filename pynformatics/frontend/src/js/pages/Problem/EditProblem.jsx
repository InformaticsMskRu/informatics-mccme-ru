import React from 'react';
import * as problemActions from '../../actions/problemActions';
import {connect} from 'react-redux';
import MainContentWrapper from '../../components/utility/MainContentWrapper';
import AceEditor from 'react-ace';
import 'brace/mode/html';
import 'brace/theme/tomorrow';
import Button from '../../components/utility/Button';
import styled from 'styled-components';
import Box from '../../components/utility/Box';
import {ProblemStatement} from "./ProblemStatement";

const ProblemWrapper = styled.div`
  > div {
    height: auto;
  }
  
  .asd {
    font-size: 100%;
    font: inherit;
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
        this.props.dispatch(problemActions.editProblem(this.state.name, this.state.code, this.problemId));
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
                        <div>Название: <input onChange={event => this.setNewName(event.target.value)} type={'text'}
                                              value={this.state.name}/></div>
                        <styledNormalize>
                            <AceEditor
                                mode='html'
                                theme='tomorrow'
                                name='blah'
                                value={this.state.code}
                                showPrintMargin={true}
                                showGutter={true}
                                highlightActiveLine={true}
                                onChange={(newCode) => this.setNewCode(newCode)}
                                setOptions={{
                                    enableBasicAutocompletion: true,
                                    enableLiveAutocompletion: true,
                                    enableSnippets: true,
                                    showLineNumbers: true,
                                }}/>
                        </styledNormalize>
                        <h3>Предпросмотр:</h3>
                        <ProblemStatement statement={this.state.code}/>
                        <Button onClick={() => this.editProblem()} type="primary">Отправить</Button>
                    </Box>
                </ProblemWrapper>
            </MainContentWrapper>
        );
    }
}

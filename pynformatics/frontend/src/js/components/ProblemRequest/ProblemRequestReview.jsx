import React from 'react';
import {connect} from 'react-redux';
import {Link, Redirect} from 'react-router-dom'

import * as problemRequestReviewActions from '../../actions/problemRequestReviewActions';
import MainContentWrapper from "../utility/MainContentWrapper";

import {split as SplitEditor} from 'react-ace';
import {diff as DiffEditor} from 'react-ace';
import AceEditor from 'react-ace';

import 'brace/mode/html';
import 'brace/theme/tomorrow';

import Box from '../../components/utility/Box';
import Button from '../../components/utility/Button';
import {
  gutter,
  colStyle,
  rowStyle,
  Col,
  Row,
} from '../../components/utility/Grid';

@connect(state => ({
  problem_request: state.problem_request_review,
}))
export default class ProblemRequestReview extends React.Component {
  constructor(props) {
    super(props);
    this.requestId = parseInt(this.props.match.params.requestId, 10);
    this.fetchRequest(this.requestId);

    this.state = {name: undefined, content: undefined, problem: ''};
  }

  fetchRequest(requestId) {
    this.props.dispatch(problemRequestReviewActions.fetchRequest(requestId));
  }

  approveRequest(requestId) {
    this.props.dispatch(problemRequestReviewActions.approveRequest(
      requestId, this.state.name, this.state.content
    ));
  }

  declineRequest(requestId) {
    this.props.dispatch(problemRequestReviewActions.declineRequest(requestId));
    //return <Redirect to="/problem_requests"/>
  }

  updateName(newName) {
    this.setState({name: newName});
  }

  updateContent(newContent) {
    this.state.content = newContent;
    //this.setState({content: newContent});
  }

  render() {
    const data = this.props.problem_request[this.requestId];

    if (!data) {
      return <MainContentWrapper>
        <div>data not found</div>
      </MainContentWrapper>
    }

    if (this.state.name === undefined) {
      this.updateName(data.name);
    }
    if (this.state.content === undefined) {
      this.updateContent(data.content);
    }

    return (
      <MainContentWrapper>
        <Box style={{height: 'auto', width: 'auto'}}>
          <Row>
            <Col md={12} type="flex" justify="center" style={colStyle}>
              <h3>До</h3>
            </Col>
            <Col md={12} type="flex" justify="center" style={colStyle}>
              <h3>После</h3>
            </Col>
          </Row>
          <Row>
            <Col md={12} style={colStyle}>
              <h3>{data.problem.name}</h3>
            </Col>
            <Col md={12} style={colStyle}>
              <div><input type="text" value={this.state.name}
                          readOnly={data.status !== "review"}
                          onChange={event => this.updateName(event.target.value)}/></div>
            </Col>
          </Row>
          <Row gutter={gutter} type="flex" justify="center" style={{...rowStyle}}>
            <DiffEditor
              mode="html"
              theme="tomorrow"
              value={[data.problem.content, this.state.content]}
              fontSize={14}
              width="900px"
              height="400px"
              editorProps={{$blockScrolling: true}}
              readOnly={data.status !== "review"}
              onChange={([oldContent, newContent]) => this.updateContent(newContent)}
            />
          </Row>
          <Row gutter={gutter} type="flex" justify="center" style={{...rowStyle, marginTop: '10px'}}>
            {data.status === "review" ? (
              <div>
                <Button onClick={() => this.approveRequest(this.requestId)}
                        type="primary" style={{marginRight: '20px'}}>
                  Принять
                </Button>
                <Button onClick={() => this.declineRequest(this.requestId)} type="primary">Отклонить</Button>
              </div>
            ) : (
              <div/>
            )}
          </Row>
        </Box>
      </MainContentWrapper>
    );
  }
}
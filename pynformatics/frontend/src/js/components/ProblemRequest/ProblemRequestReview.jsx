import React from 'react';
import {connect} from 'react-redux';
import {Link, Redirect} from 'react-router-dom'

import * as problemRequestReviewActions from '../../actions/problemRequestReviewActions';
import MainContentWrapper from "../utility/MainContentWrapper";


import Box from '../../components/utility/Box';
import Button from '../../components/utility/Button';
import {
  gutter,
  colStyle,
  rowStyle,
  Col,
  Row,
} from '../../components/utility/Grid';

import message from '../../isomorphic/components/feedback/message';
import { MonacoDiffEditor } from 'react-monaco-editor';


@connect(state => ({
  problemRequest: state.problemRequestReview,
}))
export default class ProblemRequestReview extends React.Component {
  constructor(props) {
    super(props);
    this.requestId = parseInt(this.props.match.params.requestId, 10);
    this.fetchRequest(this.requestId);

    this.state = {
      name: undefined,
      content: undefined,
      problem: '',
      approveLoading: false,
      declineLoading: false,
    };
  }

  fetchRequest(requestId) {
    this.props.dispatch(problemRequestReviewActions.fetchRequest(requestId));
  }

  approveRequest(requestId) {
    this.setState({ approveLoading: true});
    this.props.dispatch(problemRequestReviewActions.approveRequest(
      requestId, this.state.name, this.state.content
    )).then(result => {
      this.setState({ approveLoading: false});
      message.success('Изменения приняты');
    }).catch(error => {
      this.setState({ approveLoading: false});
      message.error(error.response.data.message);
    });
  }

  declineRequest(requestId) {
    this.setState({ declineLoading: true});
    this.props.dispatch(problemRequestReviewActions.declineRequest(
      requestId
    )).then(result => {
      this.setState({ declineLoading: false});
      message.success('Изменения отклонены');
    }).catch(error => {
      this.setState({ declineLoading: false});
      message.error(error.response.data.message);
    });
  }

  updateName(newName) {
    this.setState({name: newName});
  }

  updateContent(newContent) {
    this.setState({content: newContent});
  }

  render() {
    const data = this.props.problemRequest[this.requestId];

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

    const options = {
      readOnly: data.status !== "review",
      language: "html",
    };
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
            <MonacoDiffEditor
              width="900"
              height="400"
              language="html"
              original={data.problem.content}
              value={this.state.content}
              onChange={(newContent) => this.updateContent(newContent)}
              options={options}
            />
          </Row>
          <Row gutter={gutter} type="flex" justify="center" style={{...rowStyle, marginTop: '10px'}}>
            {data.status === "review" ? (
              <div>
                <Button onClick={() => this.approveRequest(this.requestId)}
                        loading={this.state.approveLoading}
                        type="primary" style={{marginRight: '20px'}}>
                  Принять
                </Button>
                <Button onClick={() => this.declineRequest(this.requestId)}
                        loading={this.state.declineLoading}
                        type="primary">
                  Отклонить
                </Button>
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
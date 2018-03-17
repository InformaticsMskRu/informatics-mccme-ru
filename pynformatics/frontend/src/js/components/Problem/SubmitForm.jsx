import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Link, withRouter } from 'react-router-dom';
import { Tag } from 'antd';
import { connect } from 'react-redux';
import { palette } from 'styled-theme';
import * as _ from 'lodash';

import Button from '../../components/utility/Button';
import CodeMirror from '../../components/utility/CodeMirror';
import Dropzone, { DropzoneWrapper } from '../../components/utility/Dropzone';
import Select, { SelectOption } from '../../components/utility/Select';
import isUserLoggedIn from "../../utils/isUserLoggedIn";
import { LANGUAGES } from '../../constants';
import { borderRadius } from '../../isomorphic/config/style-util';
import { getExtensionByFilename }  from '../../utils/functions';
import * as problemAcitons from '../../actions/problemActions';


const SubmitFormWrapper = styled.div`
  position: relative;

  & > div { margin-bottom: 10px; }

  .loginBtn {
    display: flex;
    width: 100%;
    height: 80px;
    align-items: center;
    justify-content: center;
    background: #f3f5f7;
  }
  
  .buttonsWrapper {
    display: flex;
    flex-wrap: wrap;
    width: 100%;
  
    .languageSelect {
      margin-right: 9px;
      margin-bottom: 9px;
    
      &.ant-select {
        width: 174px;
        
        .ant-select-selection {
          height: 36px !important;
        }
      }
    }
    
    .toggleTextEditBtn {
      margin-left: auto;
      margin-top: auto;
      & .ant-btn {
        background: ${palette('primary', 6)};
        border-color: ${palette('primary', 6)};
      }
      
      @media (max-width: 767px) {
        display: none;
      }
    }
  }
  
  .codeMirrorWrapper {
    width: 100%;
    padding: 14px 36px;
    background: #f3f5f7;
    border: 1px solid #f3f5f7;
    ${borderRadius('4px')};
    text-align: left;
    
    & > div { background: #ffffff; }
    
    @media (max-width: 767px) {
      padding: 0;
    }
  }
  
  .dropzoneCover {
    width: 100%;
    height: 80px;
    
    display: flex;
    justify-content: center;
    background: #f3f5f7;
    
    .ant-tag {
      margin: auto 0;
    }
  }
`;

export class SubmitForm extends React.Component {
  static contextTypes = {
    statementId: PropTypes.number,
  };

  static propTypes = {
    windowWidth: PropTypes.number.isRequired,
    problemId: PropTypes.number.isRequired,
  };

  constructor() {
    super();

    try {
      this.languageInfo = JSON.parse(localStorage.getItem('languageInfo')) || {};
    } catch (e) {
      this.languageInfo = {};
    }

    this.state = {
      languageId: _.maxBy(_.keys(this.languageInfo), id => this.languageInfo[id]) || 1,
      showCodeMirror: false,
      submitProcessed: true,
      showSubmitButtonSpinner: false,
    };

    this.toggleCodeMirror = this.toggleCodeMirror.bind(this);
    this.submitProblem = this.submitProblem.bind(this);

    this.dropzoneAddedfile = this.dropzoneAddedfile.bind(this);
  }

  toggleCodeMirror() {
    this.setState({
      ...this.state,
      showCodeMirror: !this.state.showCodeMirror,
    });
  }

  dropzoneAddedfile(file) {
    const extension = '.' + getExtensionByFilename(file.name);
    const matchExtension = _.filter(_.keys(LANGUAGES),
        id => LANGUAGES[id].extension === extension);
    const languageId = _.maxBy(matchExtension, id => this.languageInfo[id]) || this.state.languageId;
    this.setState({
      ...this.state,
      file,
      languageId,
    });
  }

  submitProblem() {
    const { languageId } = this.state;

    this.languageInfo[languageId] = (new Date()).getTime();
    localStorage.setItem('languageInfo', JSON.stringify(this.languageInfo));
    if (!this.state.file && !this.state.source) {
      alert('nothing to submit');
      return;
    }
    this.setState({showSubmitButtonSpinner: true});
    this.props.dispatch(problemAcitons.submitProblem(
      this.props.problemId,
      _.pick(this.state, ['languageId', 'file', 'source']),
      this.context.statementId,
    )).then(() => {
      this.setState({
        ...this.state,
        showSubmitSuccess: true,
        showSubmitError: false,
        showSubmitButtonSpinner: false,
      });
      setTimeout(() => this.setState({
        ...this.state,
        showSubmitSuccess: false,
      }), 2000);
    }).catch(error => {
      this.setState({
        ...this.state,
        showSubmitError: true,
        showSubmitButtonSpinner: false,
      });
      console.log(error);
    });
  }

  render() {
    const loggedIn = isUserLoggedIn(this.props.user);

    if (!loggedIn) {
      return (
        <SubmitFormWrapper>
          <div className="loginBtn">
            <Link 
              to={{
                pathname: '/auth/login',
                state: { from: this.props.location.pathname }
              }}
            >
              <Button type="primary">Войдите в систему, чтобы сдать задачу</Button>
            </Link>
          </div>
        </SubmitFormWrapper>
      )
    }

    const { windowWidth } = this.props;
    const {
      languageId,
      showCodeMirror,
      showSubmitError,
      showSubmitSuccess,
      source,
    } = this.state;
    const languageConfig = LANGUAGES[languageId];

    return (
      <SubmitFormWrapper>
        {
          showSubmitSuccess
            ? (
              <div className="dropzoneCover">
                <Tag
                  color="#87CE50"
                  onClick={() => this.setState({...this.state, showSubmitSuccess: false})}
                >
                  Решение загружено!
                </Tag>
              </div>
            ) : null
        }
        {
          showSubmitError
            ? (
              <div className="dropzoneCover">
                <Tag
                  color="#EE4E49"
                  onClick={this.submitProblem}
                >
                  Произошла ошибка. Нажмите, чтобы попробовать снова.
                </Tag>
              </div>
            ) : null
        }
        {
          !(showSubmitSuccess || showSubmitError)
          ? (
            <Dropzone
              config={{
                postUrl: 'no-url',
              }}
              djsConfig={{
                maxFiles: 1,
                autoProcessQueue: false,
              }}
              eventHandlers={{
                init: dropzone => {
                  dropzone.on('maxfilesexceeded', file => {
                    dropzone.removeAllFiles();
                    dropzone.addFile(file);
                  })
                },
                addedfile: this.dropzoneAddedfile,
              }}
            />
          ) : null
        }

        { showCodeMirror || (windowWidth && windowWidth < 768)
          ? (
            <div className="codeMirrorWrapper">
              <CodeMirror
                value={source}
                options={{
                  lineNumbers: true,
                  readOnly: false,
                  tabSize: 4,
                  mode: languageConfig.mime,
                }}
                onChange={source => this.setState({...this.state, source})}
              />
            </div>
          )
          : null }

        <div className="buttonsWrapper">
          <Select
            className="languageSelect"
            size="large"
            defaultValue={languageId}
            value={languageId.toString()}
            onChange={value => this.setState({...this.state, languageId: parseInt(value)})}
          >
            {
              _.map(LANGUAGES, (config, id) => (
                <SelectOption value={id} key={id}>{config.name}</SelectOption>
              ))
            }
          </Select>
          <Button
            type="primary"
            onClick={this.submitProblem}
            loading={this.state.showSubmitButtonSpinner}
          >
            Сдать решение
          </Button>
          <div className="toggleTextEditBtn">
            <Button
              type="primary"
              size="small"
              onClick={this.toggleCodeMirror}
            >
              Сдать код текстом
            </Button>
          </div>
        </div>
      </SubmitFormWrapper>
    );
  }
}

export default withRouter(connect(state => ({
  user: state.user,
  windowWidth: state.ui.width,
}))(SubmitForm));

import BasicDropzone from 'react-dropzone-component';
import styled from 'styled-components';
import React from 'react';
import * as _ from 'lodash';
import ReactDOMServer from 'react-dom/server';

import { borderRadius } from '../../isomorphic/config/style-util';

import { UploadIcon } from '../Icon';

const DropzoneWrapper = styled.div`
  .customDropzone {
    display: flex;
    flex-flow: row wrap;
    align-content: center;
    justify-content: center;
    
    width: 100%;
    height: 80px;
    background: #f3f5f7;
    cursor: pointer;
    ${borderRadius('4px')};
    
    & > i {
      fill: #788195;
      height: auto;
      align-self: center;
    }
    & > div {
      font-size: 16px;
      color: #788195;
      margin-left: 15px;
      align-self: center;
    }
    
    &.dz-started > *:not(.dz-preview) { display: none; }
    
    .dz-preview {
      margin: 0;
      
      .dz-filename {
        display: flex;
        span { 
          cursor: default; 
          padding-right: 20px; 
        }
      }
    }
  }
`;

const PreviewTemplate = ReactDOMServer.renderToStaticMarkup(
  <div className="dz-preview dz-file-preview">
    <div className="dz-filename">
      <span data-dz-name />
      <i className="material-icons" data-dz-remove>close</i>
    </div>
  </div>
);

const Dropzone = props => {
  _.set(props, 'config.dropzoneSelector', '.customDropzone');
  _.set(props, 'djsConfig.previewTemplate', PreviewTemplate);
  _.set(props, 'djsConfig.clickable', '.customDropzone, .customDropzone *');
  return (
    <DropzoneWrapper>
      <div className="customDropzone">
        <UploadIcon size={30} />
        <div>Выберите файл</div>
      </div>
      <BasicDropzone {...props} />
    </DropzoneWrapper>
  );
};

export default Dropzone;

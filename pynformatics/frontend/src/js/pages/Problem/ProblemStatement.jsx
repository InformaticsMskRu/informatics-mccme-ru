import React from "react";
import 'brace/mode/html';
import 'brace/theme/tomorrow';
import styled from 'styled-components';
import {palette} from 'styled-theme';

const ProblemStatementWrapper = styled.div`
  > div {
    height: auto;
  }

  .problemStatement {
    text-align: left;
    color: ${palette('other', 7)};
    
    .legend {
      p { margin-bottom: 34px; }  
    }
    
    div { 
      margin-bottom: 34px;
    
      .section-title {
        width: 100%;
        margin-bottom: 20px;
        
        display: flex;
        align-items: center;
        
        font-size: 19px;
        font-weight: 500;
        color: ${palette('secondary', 2)};
        white-space: nowrap;
        
        &:before {
          content: '';
          width: 5px;
          height: 40px;
          background: ${palette('secondary', 3)};
          display: flex;
          margin-right: 15px;
        }
        
        &:after {
          content: '';
          width: 100%;
          height: 1px;
          background: ${palette('secondary', 3)};
          display: flex;
          margin-left: 15px;
        }
      }
    }
  }
`;

export class ProblemStatement extends React.PureComponent {

    render() {
        return (
            <ProblemStatementWrapper>
                <div
                    className="problemStatement"
                    dangerouslySetInnerHTML={{__html: this.props.statement}}
                    ref={(node) => window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, node])}
                />
            </ProblemStatementWrapper>
        );
    }
}

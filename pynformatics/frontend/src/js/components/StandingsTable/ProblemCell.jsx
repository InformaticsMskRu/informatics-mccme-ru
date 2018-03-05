import React from 'react';
import styled from 'styled-components';
import { palette } from 'styled-theme';

import moment from '../../utils/moment';
import { borderRadius } from '../../isomorphic/config/style-util';
import { getProblemCellColor } from '../../utils/functions';


const ProblemCellWrapper = styled.div`
  ${({empty, score, theme}) => empty 
    ? null 
    : `background: ${getProblemCellColor(score, theme)};`
  }
  color: ${palette('other', 7)};
  display: flex;
  flex-flow: column nowrap;
  margin: auto;
  min-width: ${({small}) => small ? '22px' : '60px'};
  height: 35px;
  ${borderRadius('4px')}
  align-content: center;
  justify-content: center;

  .problemCellResult {
    line-height: normal;
    font-size: 16px;
    font-weight: bold;
  }

  .problemCellTime {
    line-height: normal;
    font-size: 10px;
  }

  ${({shrinkable}) => shrinkable
    ? `
      @media (max-width: 575px) {
        min-width: 22px;
      }
    ` : null
  }

  .problemCellEmpty {
    background: ${palette('other', 13)};
    width: 12px;
    height: 12px;
    margin: auto;
    opacity: 0.1;
  }
`;


export default ({score, attempts, time, shrinkable=true, small=false}) => {
  if (typeof attempts === 'undefined' || attempts === 0) {
    return (
      <ProblemCellWrapper 
        empty={true}
        shrinkable={shrinkable}
        small={small}
      >
        <div className="problemCellEmpty" />
      </ProblemCellWrapper>
    );
  }
  const success = score === 100;

  return (
    <ProblemCellWrapper 
      score={score} 
      shrinkable={shrinkable}
      small={small}
    >
      <div className="problemCellResult">
        {success ? '+' : '-'}{success && attempts === 1 ? '' : attempts}
      </div>
      { time 
        ? <div className="problemCellTime">{time}</div>
        : null
      }
    </ProblemCellWrapper>
  );
};

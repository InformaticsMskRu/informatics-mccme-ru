import React from 'react';
import styled, { injectGlobal } from 'styled-components';
import { palette } from 'styled-theme';

import Tooltip from '../utility/Tooltip';
import { getProblemShortNameByNumber } from '../../utils/functions';
import Box from '../utility/Box';

// TODO: https://github.com/InformaticsMskRu/informatics-mccme-ru/issues/246

injectGlobal`
  .problemColumnHeaderTooltip {
      .ant-tooltip-arrow { display: none; }

      .ant-tooltip-inner {
        background: #FFFFFF;
        padding: 20px;
        max-width: 300px;
      }
  }
`;

const TooltipTitleWrapper = styled.div`
  color: ${palette('other', 7)};

  .problemColumnHeaderTooltipTitle {
    font-size: 16px;
    // margin-bottom: 7px;
  }
  .problemColumnHeaderTooltipContent {
    font-size: 14px;
  }
`;

const TooltipTitle = ({title, content}) => (
  <TooltipTitleWrapper>
    <div className="problemColumnHeaderTooltipTitle">{title}</div>
    {/* <div className="problemColumnHeaderTooltipContent">{content}</div> */}
  </TooltipTitleWrapper>
)


export default ({rank, title, content}) => {
  const shortName = getProblemShortNameByNumber(rank);

  return (
    <Tooltip 
      title={
        <TooltipTitle 
          title={`${shortName} - ${title}`}
          content={content}
        />
      }
      placement="bottom"
      overlayClassName="problemColumnHeaderTooltip"
    >
      <span style={{cursor: 'pointer'}}>
        {shortName}
      </span>
    </Tooltip>
  );
}


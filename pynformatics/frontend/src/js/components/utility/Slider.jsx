import styled from 'styled-components';
import { Slider as AntdSlider } from 'antd';
import { palette } from 'styled-theme';


const Slider = styled(AntdSlider)`
  && {
    height: 18px;
    padding: 6px 0;

    .ant-slider-rail {
      opacity: 0.3;
      height: 6px;
      background: ${palette('other', 7)};
    }
    .ant-slider-track {
      background: none;
    }

    .ant-slider-handle {
      background: #34383C;
      border-color: #FFFFFF;
      width: 18px;
      height: 18px;
      margin-left: -9px;
      margin-top: -6px;
      box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);

      &:focus {
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
      }
    }
  }

  &&:hover {
    .ant-slider-rail {
      background: ${palette('other', 7)};
    }

    .ant-slider-track {
      background: none;
    }

    .ant-slider-handle,
    .ant-slider-handle:not(.ant-tooltip-open) {
      background: #34383C;
      border-color: #FFFFFF;
    }
  }
`;

export default Slider;

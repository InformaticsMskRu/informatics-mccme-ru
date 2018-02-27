import { palette } from 'styled-theme';

import IsoRadioBox, { 
  RadioGroup as IsoRadioGroup, 
  RadioButton as IsoRadioButton 
} from '../../isomorphic/components/uielements/radio';


const RadioBox = IsoRadioBox;

const RadioButton = IsoRadioButton.extend`
  &&:not(.ant-radio-button-wrapper-disabled) {
    background: #F7F7F7;
    border-color: #D9D9D9;
    color: #888888;
  }

  &&:not(.ant-radio-button-wrapper-disabled):hover {
    color: ${palette('other', 6)};
    border-color: ${palette('other', 6)};
  }

  &&.ant-radio-button-wrapper-checked {
    background: ${palette('other', 6)};
    color: #FFFFFF;

    &:hover { color: #FFFFFF; }
  }

`;

const RadioGroup = IsoRadioGroup;

export default RadioBox;
export { RadioGroup, RadioButton };

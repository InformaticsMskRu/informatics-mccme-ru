import React from 'react';
import styled from 'styled-components';
import { Icon } from 'antd';

import Input from '../utility/Input';


const SearchWrapper = styled.div`
  color: #ffffff;
  
  &&& .ant-input {
    background: rgba(129, 132, 145, 0.3);
    border: none;
    border-radius: 15px;
    color: #ffffff;
    padding: 0 33px 0 37px;
    min-width: 284px;
    height: 30px;
    font-family: Roboto, sans-serif;
    font-size: 15px;
    
    ::-webkit-input-placeholder { /* Chrome/Opera/Safari */
      color: rgba(255, 255, 255, 0.3);
    }
    ::-moz-placeholder { /* Firefox 19+ */
      color: rgba(255, 255, 255, 0.3);
    }
    :-ms-input-placeholder { /* IE 10+ */
      color: rgba(255, 255, 255, 0.3);
    }
    :-moz-placeholder { /* Firefox 18- */
      color: rgba(255, 255, 255, 0.3);
    }
  }
  
  .ant-input-prefix i {
    color: rgba(255, 255, 255, 0.3);
    cursor: default;
  }
  .ant-input-suffix i {
    color: #ffffff;
    cursor: pointer;
  }
`;

export default class Search extends React.Component {
  constructor() {
    super();
    this.state = {
      searchQuery: '',
    };

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    this.setState({
      searchQuery: e.target.value,
    })
  }

  render() {
    const { searchQuery } = this.state;

    const prefix = <i className="material-icons md-18">search</i>;
    const suffix = searchQuery ? <Icon type="arrow-right" /> : '';
    const placeholder = 'Найти задачу, курс или сборы';

    return (
      <SearchWrapper>
        <Input
          onChange={this.handleChange}
          prefix={prefix}
          suffix={suffix}
          placeholder={placeholder}
        />
      </SearchWrapper>
    );
  }
};

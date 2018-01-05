import React from 'react';
import styled from 'styled-components';

import Button from '../../components/utility/Button';
import Input from '../../components/utility/Input';


const SearchWrapper = styled.div`
  .inputContainer {
    overflow: hidden;
  }
  
  .buttonContainer {
    float: right;
    margin-left: 12px;
    @media (min-width: 576px) {
      margin-left: 20px;
    }  
  }
`;
const Search = () => (
  <SearchWrapper>
    <div className="buttonContainer">
      <Button type="primary" style={{float: 'right'}}>Найти</Button>
    </div>
    <div className="inputContainer">
      <Input />
    </div>
  </SearchWrapper>
);

export default Search;

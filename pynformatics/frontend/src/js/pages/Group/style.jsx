import styled from "styled-components";

// language=SCSS
const StyleWrapper = styled.div`.root-wrapper {
  background-color: #ffffff;
  border: solid 1px #e6e5e5;

  .group-header {
    height: 90px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    border-bottom: solid 1px #e6e5e5;

    .back-button {
      margin: 0 25px;
      opacity: 0.5;
    }
    .title-wrapper {
      margin-right: 25px;
      flex: 1;
      display: flex;
      justify-content: center;
    }
    .title {
      font-size: 20px;
      color: #2d3446;
    }
  }
  
  .group-body {
    padding: 0;
    border-bottom: solid 1px #e6e5e5;
    
    .group-body_column {
      padding: 25px;
      
      .header {
        opacity: 0.9;
        font-size: 18px;
        color: #343a40;
      }
    }
  }
  
  .group-add {
    .group-add_column {
      padding: 25px;
    }
  }
}`;

export default StyleWrapper;
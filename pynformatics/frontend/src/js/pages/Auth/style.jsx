import styled from "styled-components";

const StyleWrapper = styled.div`
  .wrapper {
    border-radius: 6px;
    background-color: #ffffff;
    box-shadow: 0 0 24px 0 rgba(182, 189, 197, 0.42);
    height: 100%;
  }
  
  .leftColumn {
    height: calc(100% - 32px); /* may cause problems */
  
    margin-top: 16px;
    margin-bottom: 16px;
    padding: 16px;
    border-radius: 4px;
    background-color: #f3f5f7;
  
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .leftColumn .menu {
    background-color: #f3f5f7;
    color: #788195;
    margin-bottom: 16px;
    border-right: 0;
  }
  
  .leftColumn .menu .ant-menu-item {
    padding: 0 !important; /* it's okay to use !important when you override library classes in page specific css */
    margin: 0 !important;
  }
  
  .leftColumn .menu .link {
    background-color: #f3f5f7 !important;
    color: #788195 !important;
  }
  
  .leftColumn .menu .linkActive {
    background-color: #f3f5f7 !important;
    color: #4482ff !important;
  }
  
  .form {
    margin-top: 32px;
    margin-bottom: 16px;
  }
  
  .form>* {
    margin-bottom: 16px !important;
  }
  
  .formTitle {
    font-size: 22px;
    color: #2d3446;
  }
  
  .formSubtitle {}
  
  .errorMessage {
    display: flex;
    align-items: center;
  
    min-height: 42px;
    padding: 8px;
    font-size: 14px;
    border-radius: 4px;
    border: solid 1px #fff5d5;
    background-color: #fffbee;
    color: #788195;
  }
  
  .errorMessage>span {
    margin-right: 8px;
  }
  
  @media only screen and (max-width: 767px) {
    .errorMessage {
      border: 0;
      background-color: #ff6000;
      color: #ffffff;
    }
  }
  
  .inputGroup {
    display: inline-flex;
    justify-content: flex-start;
    flex-wrap: wrap;
    align-items: center;
  }
  
  .autoComplete {
    width: 100%;
    font-size: 13px !important;
  }
  
  .socialButtonGroup {
    margin-top: 16px;
  }
  
  .mainButton {
    margin-right: 16px !important;
  }
  
  .smallButton {
    padding: 0 14px !important;
    border-radius: 3px !important;
    font-size: 12px !important;
    color: #ffffff !important;
  }
  
  .VKButton {
    margin-right: 8px !important;
    background-color: #527daf !important;
    border-color: #527daf !important;
  }
  
  .GmailButton {
    background-color: #4890f8 !important;
    border-color: #4890f8 !important;
  }
  
  .generateButton {
    padding: 0 !important;
    background-color: #90b7ff !important;
    border-color: #90b7ff !important;
    width: 100% !important;
    height: 42px !important;
    color: #ffffff !important;
  }
`;

export default StyleWrapper;
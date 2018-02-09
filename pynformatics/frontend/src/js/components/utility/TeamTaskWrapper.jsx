import MainContentWrapper from './MainContentWrapper';

const TeamTaskWrapper = MainContentWrapper.extend`
  padding-top: 86px;
  
  header1 {
    font-size: 20px;
    font-weight: normal;
    font-style: normal;
    font-stretch: normal;
    line-height: normal;
    letter-spacing: 0.6px;
    text-align: left;
    color: #393a39;
  }
  
  header2 {
    font-size: 16px;
    font-weight: normal;
    font-style: normal;
    font-stretch: normal;
    line-height: normal;
    letter-spacing: 0.6px;
    text-align: left;
    color: #2d3446;
  }
  
  div1 {
    width: 365px; 
    margin-top: 28.5px;
  }
  
  text {
     font-size: 14px;
     font-weight: normal;
     font-style: normal;
     font-stretch: normal;
     line-height: 1.5;
     letter-spacing: normal;
     text-align: left;
     color: #343a40;
  }
  
  @media (max-width: 576px) {
    padding-top: 70px;
    width: 90%;
    height: 100%;
    margin: 0 auto;
    
    text {
      width: 344px;
      font-size: 13px;
      font-weight: normal;
      font-style: normal;
      font-stretch: normal;
      line-height: 1.62;
      letter-spacing: normal;
      text-align: left;
      color: #343a40;
    }
    
    div1 {
      width: 344px; 
      margin-top: 28.5px;
      align: center;
    }
    
  }
    
  }
`;

export default TeamTaskWrapper;
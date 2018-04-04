import React from 'react';
import { Icon } from 'antd';


const FormWrapper = ({ title, subtitle, errorMessage, children }) => (
  <div className="form">
    <div className="formTitle">{title}</div>
    {subtitle
      ? <div className="formSubtitle">{subtitle}</div>
      : null}
    {errorMessage
      ? (
      <div className="errorMessage">
        <span><Icon type="exclamation-circle-o"/></span>
        {errorMessage}
      </div>
      ) : null}
    {children}
  </div>
);

export default FormWrapper;
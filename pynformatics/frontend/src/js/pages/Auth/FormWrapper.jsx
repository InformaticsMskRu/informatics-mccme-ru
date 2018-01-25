import React from "react";
import {Icon} from "antd";

import style from './style.css';

const FormWrapper = ({title, subtitle, errorMessage, children}) => (
  <div className={style.form}>
    <div className={style.formTitle}>{title}</div>
    {subtitle
      ? <div className={style.formSubtitle}>{subtitle}</div>
      : null}
    {errorMessage
      ? <div className={style.errorMessage}>
          <span><Icon type="exclamation-circle-o"/></span>{errorMessage}
        </div>
      : null}
    {children}
  </div>
);

export default FormWrapper;
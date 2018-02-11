import React from 'react';
import PropTypes from 'prop-types'


export default class BackButton extends React.Component {
  static contextTypes = {
    router: PropTypes.object,
  };

  render() {
    const { className, style } = this.props;
    return (
      <i
        className={`material-icons backBtn ${className}`}
        onClick={() => this.context.router.history.goBack()}
        style={{
          cursor: 'pointer',
          ...style
        }}
      >
        keyboard_backspace
      </i>
    );
  }
};

import PropTypes from 'prop-types';
import React from 'react';

import moment from '../../utils/moment';
import Progress from '../../components/utility/Progress';


export default class MenuTime extends React.Component {
  static propTypes = {
    collapsed: PropTypes.bool.isRequired,
    duration: PropTypes.number.isRequired,
    start: PropTypes.number.isRequired,
    headerHeight: PropTypes.number,
  };

  constructor() {
    super();

    setInterval(this.forceUpdate.bind(this), 1000);
  }

  render() {
    const {
      collapsed,
      duration,
      headerHeight,
      start,
    } = this.props;

    return (
      <div className="time">
        <div>
          {moment(start).format('D MMMM HH:mm ')}
          &mdash;
          {moment(start + duration).format(' HH:mm')}
        </div>
        <div>Сейчас {moment().format('HH:mm')}</div>
        <Progress
          percent={Math.min((Date.now() - start) / duration * 100, 100)}
          showInfo={false}
          style={(collapsed && headerHeight)
            ? {width: headerHeight - 71}
            : {}}
        />
      </div>
    );
  }
}

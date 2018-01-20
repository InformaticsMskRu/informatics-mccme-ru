import React from 'react';
import { Link } from 'react-router-dom';


const Header = ({ collapsed }) => (
  <div className="isoLogoWrapper">
    { collapsed
      ? null
      : <h3><Link to="/">Меню</Link></h3>
    }

  </div>
);

export default Header;

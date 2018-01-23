import React from 'react';
import styled from 'styled-components';

import MenuAbout from '../../svg/menu_about.svg';
import MenuAdmin from '../../svg/menu_admin.svg';
import MenuCourses from '../../svg/menu_courses.svg';
import MenuFAQ from '../../svg/menu_faq.svg';
import MenuFire from '../../svg/menu_fire.svg';
import MenuFresh from '../../svg/menu_fresh.svg';
import MenuGroups from '../../svg/menu_groups.svg';
import MenuManual from '../../svg/menu_manual.svg';
import MenuMonitors from '../../svg/menu_monitors.svg';
import MenuRating from '../../svg/menu_rating.svg';
import MenuSendings from '../../svg/menu_sendings.svg';
import MenuSettings from '../../svg/menu_settings.svg';
import MenuTop from '../../svg/menu_top.svg';


const IconWrapper = styled.i`
  text-align: center;
  display: block;
  font-size: 0;
  width: 24px;
  height: 24px;
  svg {
    max-width: 24px;
    max-height: 24px;
  }
  
  .icon-sz-18 {
    width: 18px;
    height: 18px;
    svg {
      max-width: 18px;
      max-height: 18px;
    }
  }
`;

const Icon = svg => ({ size = 24 }) => {
  return (
    <IconWrapper
      className={`icon icon-sz-${size}`}
      dangerouslySetInnerHTML={{__html: svg}}
    />
  )
};

export const MenuAboutIcon = Icon(MenuAbout);
export const MenuAdminIcon = Icon(MenuAdmin);
export const MenuCoursesIcon = Icon(MenuCourses);
export const MenuFAQIcon = Icon(MenuFAQ);
export const MenuFireIcon = Icon(MenuFire);
export const MenuFreshIcon = Icon(MenuFresh);
export const MenuGroupsIcon = Icon(MenuGroups);
export const MenuManualIcon = Icon(MenuManual);
export const MenuMonitorsIcon = Icon(MenuMonitors);
export const MenuRatingIcon = Icon(MenuRating);
export const MenuSendingsIcon = Icon(MenuSendings);
export const MenuSettingsIcon = Icon(MenuSettings);
export const MenuTopIcon = Icon(MenuTop);

import React from 'react';
import renderer from 'react-test-renderer';

// Этот импорт вызывает ошибку
// undefined:3:4584: missing '}'
// Которая ведет в IsoTopbarWrapper
// TODO: найти способ исправить
// import 'jest-styled-components';

import { Topbar } from '../Topbar';


describe('renders correctly', () => {
  it('with sidebar collapsed', () => {
    const tree = renderer.create(
      <Topbar sidebarCollapsed={true} />
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('with sidebar not collapsed', () => {
    const tree = renderer.create(
      <Topbar sidebarCollapsed={false} />
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });
});

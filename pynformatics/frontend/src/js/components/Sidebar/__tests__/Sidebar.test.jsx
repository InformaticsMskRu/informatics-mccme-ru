import React from 'react';
import renderer from 'react-test-renderer';
import 'jest-styled-components';
import { BrowserRouter } from 'react-router-dom';

import { Sidebar } from '../Sidebar';


describe('renders correctly', () => {
  it('collapsed', () => {
    const tree = renderer.create(
      <BrowserRouter>
        <Sidebar collapsed={true} windowHeight={700} />
      </BrowserRouter>
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('not collapsed', () => {
    const tree = renderer.create(
      <BrowserRouter>
        <Sidebar collapsed={false} windowHeight={700} />
      </BrowserRouter>
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });
});

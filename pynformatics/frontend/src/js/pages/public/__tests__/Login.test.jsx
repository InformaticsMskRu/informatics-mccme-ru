import React from 'react';
import renderer from 'react-test-renderer';

import Login from '../Login';


describe('renders correctly', () => {
  it('simple login', () => {
    const tree = renderer.create(
      <Login/>
    ).toJSON();

    expect(tree).toMatchSnapshot();
  });
});
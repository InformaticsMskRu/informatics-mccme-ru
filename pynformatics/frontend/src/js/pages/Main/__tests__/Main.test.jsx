import React from 'react';
import renderer from 'react-test-renderer';
import 'jest-styled-components';

import Main from '../Main';


describe('renders correctly', () => {
  afterEach(() => {
    localStorage.clear();
  });

  it('with empty localStorage', () => {
    const tree = renderer.create(
      <Main />
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('with panel open', () => {
    localStorage.setItem('uiState', JSON.stringify({
      mainPage: { panels: ['1'] }
    }));

    const tree = renderer.create(
      <Main />
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('with panel closed', () => {
    localStorage.setItem('uiState', JSON.stringify({
      mainPage: { panels: [] }
    }));

    const tree = renderer.create(
      <Main />
    ).toJSON();
    expect(tree).toMatchSnapshot();
  });
});

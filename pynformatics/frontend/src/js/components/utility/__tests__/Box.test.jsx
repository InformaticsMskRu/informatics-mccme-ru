import React from 'react';
import renderer from 'react-test-renderer';
import 'jest-styled-components';

import Box from '../Box';


describe('renders correctly', () => {
  it('when empty', () => {
    const tree = renderer.create(
      <Box />
    ).toJSON();

    expect(tree).toMatchSnapshot();
  });

  it('with title', () => {
    const tree = renderer.create(
      <Box title="Some title"/>
    ).toJSON();

    expect(tree).toMatchSnapshot();
  });

  it('with subtitle', () => {
    const tree = renderer.create(
      <Box subtitle="Some subtitle"/>
    ).toJSON();

    expect(tree).toMatchSnapshot();
  });

  it('with title and subtitle', () => {
    const tree = renderer.create(
      <Box title="Some title" subtitle="Some subtitle"/>
    ).toJSON();

    expect(tree).toMatchSnapshot();
  });

  it('with children', () => {
    const tree = renderer.create(
      <Box title="Some title" subtitle="Some subtitle">
        <div>child 1</div>
        <div>child 2</div>
      </Box>
    ).toJSON();

    expect(tree).toMatchSnapshot();
  });
});

import React from 'react';


export default ({input}) => {
    const {value, ...inputProps} = input;
    return (<input {...inputProps} type="file"/>)
}
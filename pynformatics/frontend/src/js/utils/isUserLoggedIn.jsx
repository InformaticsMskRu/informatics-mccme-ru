const isUserLoggedIn = (user) => {
  if ('firstname' in user && 'lastname' in user && 'id' in user) {
    return true;
  } else {
    return false;
  }
};

export default isUserLoggedIn;
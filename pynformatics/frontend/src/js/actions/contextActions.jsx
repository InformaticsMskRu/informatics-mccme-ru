export function setContextStatement(statementId) {
  return {
    type: 'SET_CONTEXT_STATEMENT',
    payload: statementId,
  };
}
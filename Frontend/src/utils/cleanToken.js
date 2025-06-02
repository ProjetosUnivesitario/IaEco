export const cleanToken = (token) => {
  if (!token) return "";

  let cleanedToken = token.trim();

  if (cleanedToken.startsWith('"') || cleanedToken.startsWith('\\"')) {
    cleanedToken = cleanedToken.substring(1);
  }
  if (cleanedToken.endsWith('"') || cleanedToken.endsWith('\\"')) {
    cleanedToken = cleanedToken.substring(0, cleanedToken.length - 1);
  }

  cleanedToken = cleanedToken.replace(/\\"/g, '"');

  return cleanedToken;
};

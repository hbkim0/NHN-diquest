function returnImageUrl(path) {
  console.log('getCoverImage - ', typeof(path), path);
  const pathLen = (typeof(path) !== 'undefined') ? path.length : 0;
  const returnUrl = (pathLen > 0) ? `${process.env.VUE_APP_API_BASE_URL}${path}` : require('../assets/no-image.jpg');
  return returnUrl;
}

export { returnImageUrl };
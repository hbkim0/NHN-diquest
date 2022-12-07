function getCoverImage(path) {
  console.log('getCoverImage - ', typeof(path), path);
  const pathLen = (typeof(path) !== 'undefined') ? path.length : 0;
  const returnUrl = (pathLen > 0) ? `${process.env.VUE_APP_API_BASE_URL}${path}` : require('../assets/no-image.jpg');
  return returnUrl;
}

const _ML_TASK_VALUE = {
  0: 'TEXT_DEEP_TAGGING',
  1: 'IMAGE_DEEP_TAGGING',
  2: 'VIRTUAL TRY-ON',
};

function getMLTaskName(value) {
  return _ML_TASK_VALUE[value];
}

export { getCoverImage, getMLTaskName };
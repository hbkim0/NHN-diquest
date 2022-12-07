import UtilsCrypto from './crypto';
export const storage = {
  
  session: {
    setUserData(userData) {
      userData.role = UtilsCrypto.cryptoAesEncrypt(userData.role);
      sessionStorage.setItem('userData', JSON.stringify(userData));
    },
  },
  local: {
    setUserData(userData) {
      userData.role = UtilsCrypto.cryptoAesEncrypt(userData.role);
      localStorage.setItem('userData', JSON.stringify(userData));
    },
  },
  
  getUserData() {
    let userData = localStorage.getItem('userData') ? localStorage.getItem('userData') : sessionStorage.getItem('userData')
    if(userData) {
      userData = JSON.parse(userData);
      userData.role = UtilsCrypto.cryptoAesDecrypt(userData.role);

      return userData;
    }
    return null;
  },
  removeUserData() {
    localStorage.removeItem('userData');
    sessionStorage.removeItem('userData');
  },
  getStorage() {
    let result;
    if(localStorage.getItem('userData')) {
      result = storage.local;
    } else if (sessionStorage.getItem('userData')) {
      result = storage.session;
    } else {
      result = null;
    }
    return result;
  }
}

export default storage;
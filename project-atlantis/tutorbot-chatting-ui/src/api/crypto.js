var CryptoJS = require("crypto-js");

export const Crypto = {
	cryptoAesEncrypt(value){
		var aesKey = CryptoJS.enc.Utf8.parse("b0f48588efef1cc7");
		var iv   = CryptoJS.enc.Utf8.parse("1234567890123456");
		var encrypted = CryptoJS.AES.encrypt(value, aesKey,{iv: iv}).toString();
		return encrypted;
  },
  
  cryptoAesDecrypt(value){
		var aesKey = CryptoJS.enc.Utf8.parse("b0f48588efef1cc7");
		var iv   = CryptoJS.enc.Utf8.parse("1234567890123456");
		var decrypted = CryptoJS.AES.decrypt(value, aesKey,{iv: iv}).toString(CryptoJS.enc.Utf8);
		return decrypted;
	}  
}

export default Crypto;
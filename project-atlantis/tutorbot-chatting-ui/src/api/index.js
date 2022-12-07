import axios from 'axios';
import config from '../config/config.json';

function userLogin(auth) {
	return axios.post(
		`${config.TUTORBOT_AUTH_API_URL}/api/v1/users/login/`,
		auth,
	);
}

function userLogout() {
	return axios.post(`${config.TUTORBOT_AUTH_API_URL}/api/v1/users/logout/`);
}

export { userLogin, userLogout };

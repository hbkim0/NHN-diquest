import config from '../config/config.json';
import urlJoin from 'url-join';

function getImageIUML(path) {
	const content = '채점해줘';
	let rtn_iuml = `<bubble class="icBubbleClass1"><text>채점요청 이미지 : </text><bubble class="bot_card_large"><image style="width:100px" imgSrc="${urlJoin(
		config.IMAGE_API_URL,
		path,
	)}"/><text>${content}</text></bubble></bubble>`;
	return rtn_iuml;
}

export { getImageIUML };

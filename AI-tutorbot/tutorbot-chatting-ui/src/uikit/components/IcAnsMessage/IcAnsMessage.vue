<!-- 메시지 컴포넌트 -->
<template>
	<div class="chat_area" :class="this.class" @scroll="handleScroll">
		<template v-if="messageLists">
			<div
				v-for="(item, index) in messageLists"
				:key="'message_' + index"
				:class="{
					chat_bot: position[messagePosition]['bot'] === item.author,
					chat_user: position[messagePosition]['user'] === item.author,
				}"
			>
				<template v-if="position[messagePosition]['user'] === item.author">
					<slot name="message_user_left" :item="item" />
					<div class="chat_text">
						<!-- {{ item.text }} -->
						<ic-ans-message-item
							:key="'message_item_' + index"
							:idx="index"
							:is-disabled="item.disabled"
							:item="item.json"
						/>
					</div>
					<div class="chat_date right">
						<!-- {{ moment(messageLists[index].dt).format('a h:m') }} -->
					</div>
				</template>
				<template v-else-if="position[messagePosition]['bot'] === item.author">
					<!-- 프로필 아이콘 start -->
					<div
						class="bot_profile"
						:class="
							theme.profile && theme.profile.class ? theme.profile.class : ''
						"
						:title="item.emotion"
						:style="{
							'background-image':
								theme.profile &&
								theme.profile.basic &&
								theme.profile.basic.path !== ''
									? item.emotion == '기쁨'
										? theme.profile.pleasure &&
										  theme.profile.pleasure.hasOwnProperty('useYn') &&
										  theme.profile.pleasure.useYn == 'Y'
											? `url(${theme.profile.pleasure.path})`
											: `url(${theme.profile.basic.path})`
										: item.emotion == '슬픔'
										? theme.profile.sadness &&
										  theme.profile.sadness.hasOwnProperty('useYn') &&
										  theme.profile.sadness.useYn == 'Y'
											? `url(${theme.profile.sadness.path})`
											: `url(${theme.profile.basic.path})`
										: item.emotion == '분노'
										? theme.profile.anger &&
										  theme.profile.anger.hasOwnProperty('useYn') &&
										  theme.profile.anger.useYn == 'Y'
											? `url(${theme.profile.anger.path})`
											: `url(${theme.profile.basic.path})`
										: item.emotion == '놀람'
										? theme.profile.surprised &&
										  theme.profile.surprised.hasOwnProperty('useYn') &&
										  theme.profile.surprised.useYn == 'Y'
											? `url(${theme.profile.surprised.path})`
											: `url(${theme.profile.basic.path})`
										: item.emotion == '황당'
										? theme.profile.quirky &&
										  theme.profile.quirky.hasOwnProperty('useYn') &&
										  theme.profile.quirky.useYn == 'Y'
											? `url(${theme.profile.quirky.path})`
											: `url(${theme.profile.basic.path})`
										: item.emotion == '지루함'
										? theme.profile.boredom &&
										  theme.profile.boredom.hasOwnProperty('useYn') &&
										  theme.profile.boredom.useYn == 'Y'
											? `url(${theme.profile.boredom.path})`
											: `url(${theme.profile.basic.path})`
										: `url(${theme.profile.basic.path})`
									: '',
						}"
					>
						<span class="bg_clip">챗봇명</span>
					</div>
					<!--// 프로필 아이콘 end -->
					<div class="bot_cont_wrap">
						<!-- chat 컨텐츠 start -->
						<ic-ans-message-item
							:key="'message_item_' + index"
							:idx="index"
							:is-disabled="item.disabled"
							:item="item.json"
						/>
						<!--// chat 컨텐츠 end -->
						<!-- chat foot start -->
						<slot name="message_user_right" :item="item" />
						<slot name="message_footer" :item="item">
							<div class="chat_foot">
								<div class="chat_date left">
									<!-- {{ moment(messageLists[index].dt).format('a h:m') }} -->
								</div>
							</div>
						</slot>
						<!--// chat foot end -->
					</div>
				</template>
				<template v-else-if="item.author === 'notice'">
					<div class="chat_notice_line">
						<span
							>{{ item.text }}<span>({{ item.dt }})</span></span
						>
					</div>
				</template>
			</div>

			<div v-if="wait" class="chat_bot">
				<div
					class="bot_profile"
					:class="
						theme.profile && theme.profile.class ? theme.profile.class : ''
					"
					:style="{
						'background-image':
							theme.profile &&
							theme.profile.basic &&
							theme.profile.basic.path !== ''
								? `url(${theme.profile.basic.path})`
								: '',
					}"
				>
					<span class="bg_clip">챗봇명</span>
				</div>
				<div class="bot_cont_wrap">
					<div class="bot_cont_item">
						<div class="bot_text">
							<div class="chat_loading">
								<span class="bg_clip">답변 준비중</span>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div
				v-for="row in colorList"
				:key="row.id"
				style="display: none"
				class="swatches"
			>
				<!-- 선택 class 에 on -->
				<span
					v-for="list in colorNum"
					:key="list.id"
					:class="`color-swatch ${row}-${list}`"
					tabindex="0"
				/>
			</div>
		</template>
	</div>
</template>
<script>
import { xmlParser } from '../../bridge';
import IcAnsMessageItem from './IcAnsMessageItem';
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css';
import '../../assets/css/color_palette.css';
import cssVars from 'css-vars-ponyfill';

export default {
	name: 'IcAnsMessage',
	components: {
		'ic-ans-message-item': IcAnsMessageItem,
	},
	props: {
		theme: {
			type: Object,
			default: function() {
				return {
					class: 'chat_theme_basic',
					profile: {},
					color: {},
				};
			},
		},
		chatbot: {
			default: {
				type: Object,
				default: function() {
					return { name: '', img: '' };
				},
			},
		},
		messageListData: [],
		messageList: {
			type: Array,
			default: null,
		},
		locale: {
			type: String,
			default: 'ko',
		},
		simulator: {
			type: Boolean,
			default: false,
		},
		useScroll: {
			type: Boolean,
			default: false,
		},
		wait: {
			type: Boolean,
			default: false,
		},
		messagePosition: {
			type: String,
			default: 'right',
		},
	},
	data() {
		return {
			scroll: true,
			colorList: [
				'red',
				'pink',
				'purple',
				'deep-purple',
				'indigo',
				'blue',
				'light-blue',
				'cyan',
				'teal',
				'green',
				'light-green',
				'lime',
				'yellow',
				'amber',
				'orange',
				'deep-orange',
				'brown',
				'blue-grey',
				'grey',
			],
			colorNum: [
				'10',
				'50',
				'100',
				'200',
				'300',
				'400',
				'500',
				'600',
				'700',
				'800',
				'900',
				'1000',
				'1100',
				'1200',
				'1300',
			],
			basicTextColor: null,
			basicHoverColor: null,
			basicBdHoverColor: null,
			position: {
				right: {
					bot: 'bot',
					user: 'user',
				},
				left: {
					bot: 'user',
					user: 'bot',
				},
			},
		};
	},
	computed: {
		messageLists() {
			this.messageList.forEach((row, index) => {
				row.id = index;
				row.json = this.convertIuml(row);
				//우선순위, iuml emotion속성(한글) > 답변에 설정된 emotion > 기본
				let emotion = row.json['ans_iuml_0']['@attributes']['emotion'];
				if (emotion !== undefined) {
					row.emotion = emotion;
				} else {
					if (
						row.emotion !== undefined &&
						Object.prototype.hasOwnProperty.call(
							this.theme.profile,
							row.emotion.toLowerCase(),
						)
					) {
						row.emotion = this.theme.profile[row.emotion.toLowerCase()].text;
					}
				}
			});
			return this.messageList;
		},
		class: function() {
			let classArray = [];

			classArray.push(this.theme.class);
			if (this.simulator) {
				classArray.push(' simulator');
			}
			if (!this.scroll) {
				classArray.push('overflow_hidden');
			}
			if (
				Object.prototype.hasOwnProperty.call(this.theme.profile, 'useYn') &&
				this.theme.profile.useYn == 'N'
			) {
				classArray.push('no_profile');
			}
			return classArray.toString().replace(/,/g, ' ');
		},
	},
	mounted() {
		if (this.theme.class == 'basic' && !this.theme.color) {
			// 기본값 적용
			this.theme.color = {};
			this.theme.color.basic_color_code = '#2196f3'; // --main-basic-color
			this.theme.color.bg_color_code = '#eef7fe'; // --main-bg-color
			this.theme.color.ans_color_code = '#ffffff'; // --main-ans-color
			this.theme.color.ans_border_color_code = '#eef7fe'; // --main-ans-bord-color
			this.theme.color.ans_font_color_code = '#333'; // --main-ans-font-color
			this.theme.color.qry_color_code = '#2196f3'; // --main-qry-color
			this.theme.color.qry_border_color_code = '#eef7fe'; // --main-qry-bord-color
			this.theme.color.qry_font_color_code = '#ffffff'; // --main-qry-font-color
			this.basicTextColor = '#ffffff'; // --main-basic-font-color
			this.basicHoverColor = '#1565c0'; // --main-basic-hover-color
			this.basicBdHoverColor = '#eef7fe'; // --main-basic-bd-hover-color
			this.theme.color.header_color_code = '#1565c0'; // --main-head-color
			this.theme.color.header_font_color_code = '#ffffff'; // --main-head-font-color
		}

		if (this.theme.color) {
			let themeColor = {
				basic: '#2196f3',
				basicFont: '#ffffff',
				basicHover: '#1565c0',
				basicBdHover: '#eef7fe',
				head: '#1565c0',
				headFont: '#ffffff',
				bg: '#eef7fe',
				ans: '#ffffff',
				ansFont: '#333',
				ansBord: '#eef7fe',
				qry: '#2196f3',
				qryFont: '#ffffff',
				qryBord: '#eef7fe',
			};
			if (this.theme.color.basic_color_code) {
				themeColor.basic = this.theme.color.basic_color_code;
				for (var i = 0; i < this.colorList.length; i++) {
					for (var j = 0; j < this.colorNum.length; j++) {
						var rgbCode = this.classToRgb(
							this.colorList[i] + '-' + this.colorNum[j],
						);
						let hexCode = this.rgb2hex(rgbCode.backgroundColor);
						if (hexCode.toUpperCase() == this.theme.color.basic_color_code) {
							this.basicTextColor = rgbCode.color;
							let hoverColor;
							let selectNum = parseInt(this.colorNum[j]);
							if (selectNum === 10) {
								hoverColor = selectNum + 90;
							} else if (selectNum === 50) {
								hoverColor = selectNum + 150;
							} else if (selectNum < 1100) {
								hoverColor = selectNum + 200;
							} else if (selectNum >= 1100) {
								hoverColor = 1300;
							}
							this.basicHoverColor = this.classToRgb(
								this.colorList[i] + '-' + hoverColor,
							).backgroundColor;
							this.basicBdHoverColor = this.classToRgb(
								this.colorList[i] + '-10',
							).backgroundColor;
						}
					}
				}
				themeColor.basicFont = this.basicTextColor;
				themeColor.basicHover = this.basicHoverColor;
				themeColor.basicBdHover = this.basicBdHoverColor;
			}
			if (this.theme.color.header_color_code) {
				themeColor.head = this.theme.color.header_color_code;
			}
			if (this.theme.color.header_font_color_code) {
				themeColor.headFont = this.theme.color.header_font_color_code;
			}
			if (this.theme.color.bg_color_code) {
				themeColor.bg = this.theme.color.bg_color_code;
			}
			if (this.theme.color.ans_color_code) {
				themeColor.ans = this.theme.color.ans_color_code;
			}
			if (this.theme.color.ans_font_color_code) {
				themeColor.ansFont = this.theme.color.ans_font_color_code;
			}
			if (this.theme.color.ans_border_color_code) {
				themeColor.ansBord = this.theme.color.ans_border_color_code;
			}
			if (this.theme.color.qry_color_code) {
				themeColor.qry = this.theme.color.qry_color_code;
			}
			if (this.theme.color.qry_font_color_code) {
				themeColor.qryFont = this.theme.color.qry_font_color_code;
			}
			if (this.theme.color.qry_border_color_code) {
				themeColor.qryBord = this.theme.color.qry_border_color_code;
			}

			cssVars({
				variables: {
					'--main-basic-color': themeColor.basic,
					'--main-basic-font-color': themeColor.basicFont,
					'--main-basic-hover-color': themeColor.basicHover,
					'--main-basic-bd-hover-color': themeColor.basicBdHover,
					'--main-head-color': themeColor.head,
					'--main-head-font-color': themeColor.headFont,
					'--main-bg-color': themeColor.bg,
					'--main-ans-color': themeColor.ans,
					'--main-ans-font-color': themeColor.ansFont,
					'--main-ans-bord-color': themeColor.ansBord,
					'--main-qry-color': themeColor.qry,
					'--main-qry-font-color': themeColor.qryFont,
					'--main-qry-bord-color': themeColor.qryBord,
				},
			});
		}
		// moment.locale(this.locale);
	},
	created() {
		this.eventBus.$on('ic-component-text', data => {
			this.componentText(data);
		});
		this.eventBus.$on('ic-component-button-click', data => {
			this.componentButtonClick(data);
		});
		this.eventBus.$on('ic-component-input-data', data => {
			this.componentInputData(data);
		});
		this.eventBus.$on('ic-component-checkbox-data', data => {
			this.componentCheckboxData(data);
		});
		this.eventBus.$on('ic-component-radiobutton-data', data => {
			this.componentRadiobuttonData(data);
		});
		this.eventBus.$on('ic-component-select-data', data => {
			this.componentSelectData(data);
		});

		this.eventBus.$on('ic-component-ans-message-scroll', data => {
			this.scroll = data.scroll;
		});
	},
	methods: {
		handleScroll() {
			this.eventBus.$emit('ic-input-scroll', {});
		},
		classToRgb(color) {
			let elem, style;
			elem = document.querySelector('.' + color);
			style = getComputedStyle(elem);
			return style;
		},
		rgb2hex(rgb) {
			if (rgb.search('rgb') == -1) {
				return rgb;
			} else {
				rgb = rgb.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+))?\)$/);
				// eslint-disable-next-line no-inner-declarations
				function hex(x) {
					return ('0' + parseInt(x).toString(16)).slice(-2);
				}
				return '#' + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
			}
		},
		componentButtonClick: function(data) {
			console.log('componentButtonClick', data);
			let transferText = '';
			let displayText = '';
			let tagData = '';
			let tagDqml = '';
			let chatEvent = '';
			if (data.action == 'confirm' || data.action == 'qry') {
				if (data.transferText == 'score'){
					console.log('test',this.messageList[data.idx]);
					console.log('test',this.messageList[data.idx]['icText']);
					console.log('test',this.messageList[data.idx]['icProbSet']);

					const scoreSubmit = {};
					var predictions = [];
					Object.keys(this.messageList[data.idx]['icProbSet']).forEach(
								(key,index) => {
									predictions.push({'prob_num':key,'answers':this.messageList[data.idx]['icProbSet'][key]});
								}
					);
					scoreSubmit.page_id = this.messageList[data.idx]['icText'].pageId;
					scoreSubmit.log_id = this.messageList[data.idx]['icText'].logId;
					scoreSubmit.predictions = predictions;
					console.log('data.data.action == score', JSON.stringify(scoreSubmit));
					const messageParams = {
						idx: data.idx,
						transferText: data.displayText,
						displayText: data.displayText,
						dqml: {submit: JSON.stringify(scoreSubmit)}
					};
					this.$emit('componentMessage', messageParams);
				} else if (data.transferText == 'prob') {
					let keyList = ['bookTitle','page','problem'];
					let probSubmit = {};
					Object.keys(this.messageList[data.idx]['icSendMsg']).forEach(
								(key,index) => {
									probSubmit[keyList[index]] = this.messageList[data.idx]['icSendMsg'][key].transferText;
								}
					);
					if(!probSubmit.bookTitle){
						alert('교재이름을 확인해주세요.');
						return;
					}else if(!probSubmit.page){
						alert('쪽수를 확인해주세요.');
						return;
					}else if(!probSubmit.problem){
						alert('문제번호를 확인해주세요.');
						return;
					};
					console.log('data.data.action == prob', JSON.stringify(probSubmit));
					const messageParams = {
						idx: data.idx,
						transferText: '문제 질문 입력',
						displayText: data.displayText,
						dqml: probSubmit,
					};
					this.$emit('componentMessage', messageParams);
				} else {
					if (
						!this.messageList[data.idx]['icSendMsg'] ||
						(this.messageList[data.idx]['icSendMsg'] && data.transferText_real)
					) {
						transferText = data.transferText;
						displayText = data.displayText;
						if (data.data) {
							tagData = data.data;
						}
						if (data.dqml) {
							tagDqml = data.dqml;
						}
						if (data.chat_event_id) {
							chatEvent = data.chat_event_id;
						}
					} else {
						if (
							Object.keys(this.messageList[data.idx]['icSendMsg']).length == 1
						) {
							Object.keys(this.messageList[data.idx]['icSendMsg']).forEach(
								key => {
									console.log(this.messageList[data.idx]['icSendMsg'][key]);
									transferText = this.messageList[data.idx]['icSendMsg'][key]
										.transferText;
									displayText = this.messageList[data.idx]['icSendMsg'][key]
										.displayText;
								},
							);
						}
					}

					const messageParams = {
						idx: data.idx,
						transferText: transferText,
						displayText: displayText,
						result: this.messageList[data.idx]['icSendMsg'],
					};

					if (tagData) {
						messageParams.data = tagData;
					}

					if (tagDqml) {
						messageParams.dqml = tagDqml;
					}

					if (chatEvent) {
						messageParams.chatEventId = chatEvent;
					}
					console.log('messageParams', messageParams);
					this.$emit('componentMessage', messageParams);
				}
			}
		},
		componentText: function(data) {
			const icText = this.messageList[data.idx]['icText']
				? this.messageList[data.idx]['icText']
				: Object();

			icText[data.key] = data.value;
			this.messageList[data.idx]['icText'] = icText;
		},
		componentInputData: function(data) {
			const icProbSet = this.messageList[data.idx]['icProbSet']
				? this.messageList[data.idx]['icProbSet']
				: Object();
			icProbSet[data.probSet.prob_num] = data.probSet.answer;
			this.messageList[data.idx]['icProbSet'] = icProbSet;

			const icSendMsg = this.messageList[data.idx]['icSendMsg']
				? this.messageList[data.idx]['icSendMsg']
				: Object();

			icSendMsg[data.nodeId] = data;
			this.messageList[data.idx]['icSendMsg'] = icSendMsg;
			if (data.action == 'qry') {
				this.componentButtonClick(data);
			}
		},
		componentCheckboxData: function(data) {
			const icSendMsg = this.messageList[data.idx]['icSendMsg']
				? this.messageList[data.idx]['icSendMsg']
				: Object();
			if (data.transferText == '' && data.displayText == '') {
				delete icSendMsg[data.nodeId];
			} else {
				icSendMsg[data.nodeId] = data;
				this.messageList[data.idx]['icSendMsg'] = icSendMsg;
			}
		},
		componentRadiobuttonData: function(data) {
			const icSendMsg = this.messageList[data.idx]['icSendMsg']
				? this.messageList[data.idx]['icSendMsg']
				: Object();
			icSendMsg[data.nodeId] = data;
			this.messageList[data.idx]['icSendMsg'] = icSendMsg;
		},
		componentSelectData: function(data) {
			const icSendMsg = this.messageList[data.idx]['icSendMsg']
				? this.messageList[data.idx]['icSendMsg']
				: Object();

			icSendMsg[data.nodeId] = data;
			this.messageList[data.idx]['icSendMsg'] = icSendMsg;
		},
		convertIuml: function(item) {
			if (!item.iuml) {
				item.iuml = item.text;
			}
			const json = xmlParser(item.iuml);
			return json;
		},
	},
	beforeDestroy(){
		// eventBus off
        this.eventBus.$off('ic-component-text');
		this.eventBus.$off('ic-component-button-click');
		this.eventBus.$off('ic-component-input-data');
		this.eventBus.$off('ic-component-checkbox-data');
		this.eventBus.$off('ic-component-radiobutton-data');
		this.eventBus.$off('ic-component-select-data');
		this.eventBus.$off('ic-component-ans-message-scroll');
    },
};
</script>

<style>
:root {
	--main-basic-color: #2196f3;
	--main-basic-font-color: #ffffff;
	--main-basic-hover-color: #1565c0;
	--main-basic-bd-hover-color: #eef7fe;
	--main-head-color: #1565c0;
	--main-head-font-color: #ffffff;
	--main-bg-color: #eef7fe;
	--main-ans-color: #ffffff;
	--main-ans-font-color: #333;
	--main-ans-bord-color: #eef7fe;
	--main-qry-color: #2196f3;
	--main-qry-font-color: #ffffff;
	--main-qry-bord-color: #eef7fe;
}
.dynamic_demo {
	overflow: hidden;
}
.scroller {
	height: 100%;
}
.bot_btnset.half:after {
	display: table;
	content: '';
	clear: both;
}

.bot_cont_item.bot_text {
	display: table !important;
}
</style>

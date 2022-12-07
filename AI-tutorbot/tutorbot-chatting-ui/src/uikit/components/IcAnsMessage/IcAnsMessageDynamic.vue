<template>
	<ic-ans-chat-screen :theme="theme">
		<template v-if="messageList">
			<dynamic-scroller
				v-if="useScroll"
				:items="messageList"
				:min-item-size="60"
				class="scroller"
			>
				<template v-slot="{ item, index, active }">
					<dynamic-scroller-item
						:item="item"
						:index="index"
						:active="active"
						:data-active="active"
						:data-index="index"
						:size-dependencies="[item.id]"
					>
						<div
							v-if="item.author == 'user'"
							class="chat_user"
							:key="'message_' + index"
						>
							<div class="chat_text">{{ item.text }}</div>
							<div class="chat_date right">
								<!-- {{ moment(messageList[index].dt).format('a h:m') }} -->
							</div>
						</div>
						<div
							v-if="item.author == 'bot'"
							class="chat_bot"
							:key="'message_' + index"
						>
							<!-- 프로필 아이콘 start -->
							<div class="bot_profile">
								<span class="bg_clip">챗봇명</span>
							</div>
							<!--// 프로필 아이콘 end -->
							<div class="bot_cont_wrap">
								<!-- chat 컨텐츠 start -->
								<ic-ans-message-item
									:idx="index"
									:item="convertIuml(item.iuml)"
									:key="'message_item_' + index"
								></ic-ans-message-item>
								<!--// chat 컨텐츠 end -->
								<!-- chat foot start -->
								<slot name="footer" v-bind:item="item">
									<div class="chat_foot">
										<div class="chat_date left">
											<!-- {{ moment(messageList[index].dt).format('a h:m') }} -->
										</div>
									</div>
								</slot>
								<!--// chat foot end -->
							</div>
						</div>
					</dynamic-scroller-item></template
				></dynamic-scroller
			>
			<template v-else>
				<div
					v-for="(item, index) in messageList"
					:key="'message_' + index"
					:class="{
						chat_bot: item.author == 'bot',
						chat_user: item.author == 'user',
					}"
				>
					<template v-if="item.author == 'user'">
						<div class="chat_text">{{ item.text }}</div>
						<div class="chat_date right">
							<!-- {{ moment(messageList[index].dt).format('a h:m') }} -->
						</div>
					</template>
					<template v-else-if="item.author == 'bot'">
						<!-- 프로필 아이콘 start -->
						<div class="bot_profile">
							<span class="bg_clip">챗봇명</span>
						</div>
						<!--// 프로필 아이콘 end -->
						<div class="bot_cont_wrap">
							<!-- chat 컨텐츠 start -->
							<ic-ans-message-item
								:idx="index"
								:item="convertIuml(item.iuml)"
								:key="'message_item_' + index"
							></ic-ans-message-item>
							<!--// chat 컨텐츠 end -->
							<!-- chat foot start -->
							<slot name="footer" v-bind:item="item">
								<div class="chat_foot">
									<div class="chat_date left">
										<!-- {{ moment(messageList[index].dt).format('a h:m') }} -->
									</div>
								</div>
							</slot>
							<!--// chat foot end -->
						</div>
					</template>
				</div>
			</template>
		</template>
	</ic-ans-chat-screen>
</template>

<script>
import { DynamicScroller, DynamicScrollerItem } from 'vue-virtual-scroller';
import { xmlParser } from '../../bridge';
import IcAnsChatScreen from '../IcAnsChatScreen';
import IcAnsMessageItem from './IcAnsMessageItem';
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css';
export default {
	name: 'ic-ans-message',
	components: {
		'ic-ans-chat-screen': IcAnsChatScreen,
		'ic-ans-message-item': IcAnsMessageItem,
		'dynamic-scroller': DynamicScroller,
		'dynamic-scroller-item': DynamicScrollerItem,
	},
	props: {
		theme: {
			type: Object,
			default: function() {
				return { class: 'chat_theme_basic', profile: {}, color: {} };
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
		useScroll: {
			type: Boolean,
			default: false,
		},
	},
	data() {
		return {};
	},
	mounted() {
		// this.moment.locale = this.locale;
	},
	created() {
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
		this.messageList.forEach((row, index) => {
			row.id = index;
		});
	},
	computed: {
		/*	messageLists() {
			this.messageList.forEach((row, index) => {
				row.id = index;
			});
			return this.messageList;
		},*/
	},
	methods: {
		componentButtonClick: function(data) {
			let transferText = '';
			let displayText = '';
			if (data.action == 'confirm' || data.action == 'qry') {
				if (!this.messageList[data.idx]['icSendMsg']) {
					transferText = data.transferText;
					displayText = data.displayText;
				} else {
					if (
						Object.keys(this.messageList[data.idx]['icSendMsg']).length == 1
					) {
						Object.keys(this.messageList[data.idx]['icSendMsg']).forEach(
							key => {
								transferText = this.messageList[data.idx]['icSendMsg'][key]
									.displayText;
								displayText = this.messageList[data.idx]['icSendMsg'][key]
									.transferText;
							},
						);
					}
				}
				this.$emit('componentMessage', {
					idx: data.idx,
					transferText: transferText,
					displayText: displayText,
					data: this.messageList[data.idx]['icSendMsg'],
				});
			}
		},
		componentInputData: function(data) {
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

			icSendMsg[data.nodeId] = data;
			this.messageList[data.idx]['icSendMsg'] = icSendMsg;
		},
		componentRadiobuttonData: function(data) {
			/*
			const icSendMsg = this.messageList[data.idx]['icSendMsg']
				? this.messageList[data.idx]['icSendMsg']
				: Object();
				*/
			const icSendMsg = Object();
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
		convertIuml: function(xml) {
			return xmlParser(xml);
		},
	},
};
</script>

<style>
.dynamic_demo {
	overflow: hidden;
}
.scroller {
	height: 100%;
}
</style>

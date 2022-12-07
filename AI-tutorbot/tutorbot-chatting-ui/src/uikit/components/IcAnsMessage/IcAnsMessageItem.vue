<template>
	<component
		v-if="getComponentName()"
		:is="'ic-ans-' + getComponentName()"
		:idx="idx"
		:attribute="getComponentAttribute()"
		:nodeId="getComponentNodeId()"
		:isDisabled="isDisabled"
		:autoClick="isAutoClick == true ? isAutoClick : autoClick"
	>
		<template v-show="isOpen" v-if="isFolder">
			<ic-ans-message-item
				v-for="(child, index) in getChildNodeKey(item)"
				:key="'item_' + index"
				:idx="idx"
				:isDisabled="isDisabled"
				:autoClick="isAutoClick == true ? isAutoClick : autoClick"
				:item="getChildNode(child)"
				:slot="getComponentSlotName()"
				@make-folder="$emit('make-folder', $event)"
				@add-item="$emit('add-item', $event)"
			></ic-ans-message-item>
		</template>
	</component>
</template>
<script>
import {
	IcAnsButton,
	IcAnsBubble,
	IcAnsText,
	IcAnsHtml,
	IcAnsCheckbox,
	IcAnsImage,
	IcAnsInput,
	IcAnsIuml,
	IcAnsLayout,
	IcAnsRadioButton,
	IcAnsSelect,
	IcAnsModal,
	IcAnsLayoutPaging,
	IcAnsLayoutPopup,
	IcAnsLayoutTable,
	IcAnsCarousel,
	IcAnsListLayout,
	IcAnsDatePicker,
	IcAnsLayoutList,
	IcAnsInfoList,
	IcAnsLink,
} from '../index';

export default {
	name: 'ic-ans-message-item',
	components: {
		'ic-ans-button': IcAnsButton,
		'ic-ans-bubble': IcAnsBubble,
		'ic-ans-text': IcAnsText,
		'ic-ans-html': IcAnsHtml,
		'ic-ans-checkbox': IcAnsCheckbox,
		'ic-ans-image': IcAnsImage,
		'ic-ans-input': IcAnsInput,
		'ic-ans-iuml': IcAnsIuml,
		'ic-ans-layout': IcAnsLayout,
		'ic-ans-radiobutton': IcAnsRadioButton,
		'ic-ans-select': IcAnsSelect,
		'ic-ans-modal': IcAnsModal,
		'ic-ans-layout-paging': IcAnsLayoutPaging,
		'ic-ans-layout-popup': IcAnsLayoutPopup,
		'ic-ans-layout-table': IcAnsLayoutTable,
		'ic-ans-carousel': IcAnsCarousel,
		'ic-ans-list-layout': IcAnsListLayout,
		'ic-ans-datepicker': IcAnsDatePicker,
		'ic-ans-info-list': IcAnsInfoList,
		'ic-ans-layout-list': IcAnsLayoutList,
		'ic-ans-link': IcAnsLink,
	},
	props: {
		idx: Number,
		item: Object,
		autoClick: Boolean,
		isDisabled: Boolean,
	},
	data() {
		return {
			isOpen: false,
			isAutoClick: false,
		};
	},
	computed: {
		isFolder: function() {
			var temp = [];
			if (Object.keys(this.item).length == 1) {
				temp = this.item[Object.keys(this.item)];
			} else {
				temp = Object.keys(this.item);
			}
			var length = 0;
			if (temp) {
				Object.keys(temp).forEach(key => {
					if (key.indexOf('@') == -1) {
						length++;
					}
				});
				return length;
			} else {
				return 0;
			}
		},
	},
	methods: {
		getComponentSlotName: function() {
			if (Object.keys(this.item).length == 1) {
				return null; // this.item[Object.keys(this.item)]['@slotName'];
			} else {
				return this.item['@slotName'];
			}
		},
		getComponentItem: function() {
			const node = Array();
			var temp = [];
			if (Object.keys(this.item).length == 1) {
				// code
			} else {
				temp = Object.keys(this.item);
			}

			temp.forEach(key => {
				if (key.indexOf('@') == -1) {
					node.push({
						slotName: key,
					});
				}
			});
			return node;
		},
		getComponentTextContent: function() {
			let textContent = '';
			if (Object.keys(this.item).length == 1) {
				// code
			} else {
				textContent = this.item['@textContent'];
			}
			return textContent;
		},
		getComponentAttribute: function() {
			const attribute = Object();
			if (Object.keys(this.item).length == 1) {
				// code
				Object.keys(this.item.ans_iuml_0['@attributes']).forEach(key => {
					attribute[key] = this.item.ans_iuml_0['@attributes'][key];
				});
			} else {
				Object.keys(this.item['@attributes']).forEach(key => {
					attribute[key] = this.item['@attributes'][key];
				});
			}
			return attribute;
		},
		getComponentNodeId: function() {
			let nodeId = '';
			if (Object.keys(this.item).length == 1) {
				nodeId = this.item[Object.keys(this.item)]['@nodeId'];
			} else {
				nodeId = this.item['@nodeId'];
			}

			return nodeId;
		},
		getComponentName: function() {
			const tags = [
				'button',
				'checkbox',
				'image',
				'input',
				'radiobutton',
				'select',
				'text',
				'bubble',
				'layout',
				'layout-table',
				'layout-paging',
				'layout-list',
				'info-list',
				'link',
				'layout-popup',
				'modal',
				'iuml',
				'html',
			];

			let nodeName = '';
			if (Object.keys(this.item).length == 1) {
				nodeName = this.item[Object.keys(this.item)]['@nodeName'];
			} else {
				nodeName = this.item['@nodeName'];
			}

			if (tags.indexOf(nodeName) >= 0) {
				return nodeName;
			} else {
				return null;
			}
		},
		getChildNode: function(child) {
			var temp = [];
			if (Object.keys(this.item).length == 1) {
				temp = this.item[Object.keys(this.item)];
			} else {
				temp = this.item;
			}
			return temp[child];
		},
		getChildNodeKey: function(child) {
			var temp = [];
			if (Object.keys(child).length == 1) {
				temp = Object.keys(child[Object.keys(child)]);
			} else {
				temp = Object.keys(child);
			}

			var node = [];
			temp.forEach(key => {
				if (key.indexOf('@') == -1) {
					node.push(key);
				}
			});
			return node;
		},
		toggle: function() {
			if (this.isFolder) {
				this.isOpen = !this.isOpen;
			}
		},
		makeFolder: function() {
			if (!this.isFolder) {
				this.$emit('make-folder', this.item);
				this.isOpen = true;
			}
		},
	},
	created() {
		if (this.item['ans_iuml_0']) {
			this.isAutoClick = this.item['ans_iuml_0']['@autoClick'];
		}
	},
	mounted() {},
};
</script>

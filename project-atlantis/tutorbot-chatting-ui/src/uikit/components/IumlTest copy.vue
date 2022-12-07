<template>
	<div class="chat_bot">
		<li v-if="this.item">
			<div :class="{ bold: isFolder }" @click="toggle" @dblclick="makeFolder">
				<template v-if="Object.keys(item).length == 1">
					{{ item[Object.keys(item)]['@nodeName'] }}
				</template>
				<template v-else>{{ item['@nodeName'] }}</template>
				<!--
				{{
					item['@nodeName']
						? item['@nodeName']
						: item[Object.keys(item)]['@nodeName']
				}}
				-->
				<!--
				{{ Object.keys(item) }}
				{{ item[Object.keys(item)]['@nodeName'] }}
				-->
				<span v-if="isFolder">[{{ isOpen ? '-' : '+' }}]</span>
			</div>
			<!-- { Object.keys(item[Object.keys(item)]) }}
			{{ item[Object.keys(item)]['ans_bubble_0'] }} -->
			<ul v-show="isOpen" v-if="isFolder">
				<ic-ans-iuml-test
					class="item"
					v-for="(child, index) in getChildNodeKey(item)"
					:key="index"
					:item="getChildNode(child)"
					@make-folder="$emit('make-folder', $event)"
					@add-item="$emit('add-item', $event)"
				></ic-ans-iuml-test>
				<li class="add" @click="$emit('add-item', item)">+</li>
			</ul>
		</li>
	</div>
</template>
<script>
import Iuml from './Iuml';
import Bubble from './Bubble';
import Text from './Text';

export default {
	name: 'ic-ans-iuml-test',
	components: {
		// eslint-disable-next-line vue/no-unused-components
		'ic-ans-iuml': Iuml,
		// eslint-disable-next-line vue/no-unused-components
		'ic-ans-button': Bubble,
		// eslint-disable-next-line vue/no-unused-components
		'ic-ans-text': Text,
	},
	props: {
		item: Object,
	},
	data() {
		return {
			isOpen: false,
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
	mounted() {},
};
</script>

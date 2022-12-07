<template>
	<div class="chat_wrapper" id="chat_wrapper">
		<div class="chat_area" :class="this.class">
			<slot></slot>
		</div>
	</div>
</template>
<script>
export default {
	name: 'ic-ans-chat-screen',
	props: {
		theme: {
			type: Object,
			default: function() {
				return { class: 'chat_theme_basic', profile: {}, color: {} };
			},
		},
		scroll: {
			type: Boolean,
			default: true,
		},
	},
	mounted() {},
	computed: {
		class: function() {
			let classArray = [];

			classArray.push(this.theme.class);
			if (!this.scroll) {
				classArray.push('overflow_hidden');
			}

			return classArray.toString().replace(/,/g, ' ');
		},
	},
};
</script>
<style>
.chat_wrapper .chat_area.overflow_hidden {
	overflow: scroll !important;
	/* overflow-y: hidden !important; */
}

.chat_wrapper .chat_modal.slide .chat_modal_in {
}

.chat_wrapper .overflow_hidden ~ .chat_modal.slide .chat_modal_in {
	bottom: 0 !important;
}

.chat_wrapper .chat_modal.flexible .chat_modal_in {
	border-radius: 10px;
	left: 5%;
	right: 5%;
}
</style>

<template>
	<div id="app">
		<router-view :key="$route.fullPath" />
	</div>
</template>

<script>
// eslint-disable-next-line no-undef
require('es6-promise').polyfill();

export default {
	name: 'app',
	mounted() {
		// this.inspectHealth();
	},
	methods: {
		inspectHealth() {
			this.$axios.post('/inspect/health').then(function() {
				//console.log("inspectHeadlth..OK");
			});
		},
	},
};
</script>

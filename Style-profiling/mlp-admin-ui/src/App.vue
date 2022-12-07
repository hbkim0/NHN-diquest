<template>
  <v-app id="inspire">
    <!-- left nav menu -->
    <v-navigation-drawer app>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="d-flex align-center text-h6">
            <router-link to="/">
              <v-img
                :src="require('./assets/diquest.png')"
                class="my-3"
                contain
              />
            </router-link>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list
        rounded
      >
        <v-list-item-group
          v-model="selectedItem"
          color="primary"
        >
          <v-list-item
            v-for="nav in navs"
            :key="nav.title"
            link
            :to="nav.to"
          >
            <v-list-item-content>
              <v-list-item-title>{{ nav.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <!-- main -->
    <v-main>
      <!-- main top -->
      <v-app-bar class="grey lighten-5" dense flat color="white">
        <v-icon>
          mdi-earth
        </v-icon>
        <v-breadcrumbs
          :items="breadcrumbs"
          divider=">"
        ></v-breadcrumbs>
      </v-app-bar>
      <!-- main container -->
      <v-container fluid class="pa-4 mb-14">
        <router-view :key="$route.fullPath"/>
      </v-container>

    </v-main>

    <v-footer padless color="white">
      <v-col
        class="text-right grey lighten-5 rounded-0"
        cols="12"
      >
        ⓒNHN diquest inc All Rights Reserved.
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  computed: {
    breadcrumbs() {
      let breadcrumbs = [];
      if (this.$route.meta) {
        let b = this.$route.meta.breadcrumbs;
        if (typeof b === 'function') {
          breadcrumbs = b(this.$route);
        } else if (Array.isArray(b)) {
          breadcrumbs = b;
        }
      }
      return breadcrumbs;
    },
  },
  data: () => ({
    selectedItem: null,
    navs: [
      { title: 'ML Task', to: '/mltask' },
      { title: 'Dataset', to: '/datasets' },
      { title: 'Annotation', to: '/annotations' },
      { title: 'Versioned Dataset', to: '/versioneddatasets' },
      { title: 'Experiment', to: '/experiments' },
      { title: 'System', to: '/system' },
    ],
    right: null,
  }),
};
</script>

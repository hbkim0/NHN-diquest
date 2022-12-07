<template>
  <v-app>
    <v-overlay z-index="10" :value="modal.show">
      <v-snackbar shaped elevation="8" color="error" multi-line timeout="-1" :value="modal.show">
        <div class="text-subtitle-1"><b>{{modal.title}}</b></div>
        <div class="text-caption">{{modal.text}}</div>
        <template v-slot:action="{ attrs }">
          <v-btn text v-bind="attrs" @click="closeModal">확인</v-btn>
        </template>
      </v-snackbar>
    </v-overlay>
    <v-snackbar shaped elevation="8" color="warning" multi-line v-model="snackbar.show">
      <div class="text-subtitle-1"><b>{{snackbar.title}}</b></div>
      <div class="text-caption">{{snackbar.text}}</div>
        <template v-slot:action="{ attrs }">
          <v-btn text v-bind="attrs" @click="snackbar.show = false">확인</v-btn>
        </template>
    </v-snackbar>

    <v-navigation-drawer app permanent>
      <v-list-item>
        <v-list-item-content>
          <router-link to="/">
            <v-img src="./assets/diquest.png" height="24px" position="left" contain />
          </router-link>
          <v-list-item-title>자동채점</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>
      <!-- -->

      <v-list>
        <v-list-item
          dense
          link
          v-for="menu in menus"
          :key="menu.title"
          :to="menu.to"
        >
          <v-list-item-icon>
            <v-icon>{{ menu.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ menu.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

    </v-navigation-drawer>

    <v-main>
      <v-app-bar dense flat>
        <v-breadcrumbs large :items="breadcrumbs" />
      </v-app-bar>

      <v-container fluid class="pa-4 mb-16">
        <router-view/>
      </v-container>

      <v-footer absolute padless>
        <v-card flat width="100%">
          <v-card-text class="text-center">
            <v-icon>mdi-copyright</v-icon>NHN diquest Inc. All Rights Reserved.
          </v-card-text>
        </v-card>
      </v-footer>
    </v-main>

  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    menus: [
      {title: "문제집 관리", icon: "mdi-book-open-variant", to: '/workbooks'},
      {title: "테스트", icon: "mdi-card-search-outline", to: '/test'},
      {title: "로그", icon: "mdi-history", to: '/logs'},
      {title: "시스템", icon: "mdi-help-network", to: '/system'},
    ],

    modal: {
      show: false,
      title: '',
      text: '',
      location: {name: ''},
    },
    snackbar: {
      show: false,
      title: '',
      text: '',
    }
  }),

  created() {
    this.$eventBus.$on('show-modal', this.showModal);
    this.$eventBus.$on('show-snackbar', this.showSnackbar);
  },

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

  methods: {
    //
    closeModal() {
      this.modal.show = false;

      if (this.modal.location) {
        this.$router.replace(this.modal.location);
      }
    },
    showModal({title, text, location}) {
      //
      this.modal.title = title || '';
      this.modal.text = text || '';
      this.modal.location = location;

      //
      this.modal.show = true;
    },

    //
    showSnackbar({title, text}) {
      //
      this.snackbar.title = title || '';
      this.snackbar.text = text || '';

      //
      this.snackbar.show = true;
    },
  }
};
</script>

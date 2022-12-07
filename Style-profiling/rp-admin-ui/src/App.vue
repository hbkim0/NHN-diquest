<template>
  <v-app id="inspire">
    <!-- left nav menu -->
    <v-navigation-drawer app>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="d-flex align-center text-h6">
            <v-img
              :src="require('./assets/diquest.png')"
              class="my-3"
              contain
              @click="moveMain"
            />
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>
      
      <v-list rounded>
        <v-list-item-group
          v-model="selectedItem"
          color="primary"
        > 
          <template v-for="nav in navs">
            <v-list-item
              v-if="!nav.subs"
              :key="nav.title"
              :value="nav.title"
              link
              :to="nav.to"
            >
              <v-list-item-content>
                <v-list-item-title>{{ nav.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>

            <v-list-group
              v-else
              :key="nav.title"
              @click="moveSub(nav.title)"
              no-action
            >
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title>{{ nav.title }}</v-list-item-title>
                </v-list-item-content>
              </template>

              <v-list-item
                v-for="sub in nav.subs"
                :key="sub.title"
                :value="sub.title"
                link
                :to="sub.to"
              >
                <v-list-item-content>
                  <v-list-item-title>{{ sub.title }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-group>
          </template>
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
    toggle: {
      dataset: false,
    },
    navs: [
      { title: 'Status', to: '/status' },
      { 
        title: 'Dataset', 
        to: '/datasets', 
        subs: [
          {title: 'Customer', to: '/customers'},
          {title: 'Product', to: '/products'},
          {title: 'History', to: '/histories'},
        ]
      },
      { title: 'Experiment', to: '/experiments' },
      { title: 'Monitoring', to: '/monitoring' },
      { title: 'Simulation', to: '/simulations' },
      { title: 'System', to: '/system' },
    ],
    right: null,
  }),
  methods: {
    moveSub(title) {
      if (title === 'Dataset') {
        this.toggle[title] = !this.toggle[title];
        if (this.toggle[title]) {
          // workaround - 현재 페이지가 CustomerView에서 다시 CustomerView를 호출할 경우 Router duplicate Error 발생을 없애기 위해 catch적용
          this.$router.push({name: 'CustomerView'}).catch(()=>{});
        }
      }
    },
    moveMain() {
      this.$store.dispatch('INIT_STATE')
        .then(res => {
          this.$router.push({path: '/'});
        })
        .catch(error => { console.log(error) });
    }
  }
};
</script>

<style scoped>
  .test {
    background-color: currentColor;
    bottom: 0;
    content: "";
    left: 0;
    pointer-events: none;
    position: absolute;
    right: 0;
    top: 0;
  }
</style>
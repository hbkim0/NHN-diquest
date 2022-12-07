<template>
  <v-container fluid>
    <v-tabs
      v-model="tab.selected"
      grow
      background-color="transparent"
      color="basil"
    >
      <v-tab
        v-for="title in tab.titles"
        :key="title"
      >
        {{ title }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab.selected">
      <!-- Detail -->
      <v-tab-item>
        <v-card
          class="pb-5"
          outlined
        >
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="text-h7 mb-1">
                <strong>
                  {{product.label}} > {{product.gender}}
                </strong>
              </v-list-item-title>
              <v-list-item-title class="text-h5 mb-1">
                {{product.name}}
              </v-list-item-title>
              <v-list-item-content v-html="htmlDescription">
              </v-list-item-content>
            </v-list-item-content>
            <v-card 
              class="ma-5 pa-5"
              elevation="3"
              outlined
            >
              <v-list-item-avatar
                tile
                size="400"
              >
                <img
                  :src="returnImageUrl(product.image)"
                >
              </v-list-item-avatar>
            </v-card>
          </v-list-item>
          
          <!-- 속성들 -->
          <v-list-item v-for="(attribute,index) in product.attributes" :key="index">
            <v-list-item-action class="mr-2">
              <v-icon>mdi-chevron-right</v-icon>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-subtitle>{{ attribute.key }} : {{ attribute.values.join(', ') }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          
        </v-card>
      </v-tab-item>
      <!-- Text tagging -->
      <v-tab-item>
        <v-card
          outlined
          class="pb-5"
        >
          <v-card-text class="pb-0">
            <v-textarea
              class="pa-0"
              outlined
              readonly
              hide-details
              name="input-7-4"
              height="400"
              label="Name, Description"
              :value="`${product.name}\n\r${product.description}`"
            ></v-textarea>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn
              large
              color="primary"
              @click="textDeepTagging"
            >
              DEEP TAGGING
            </v-btn>
          </v-card-actions>
          
          <v-divider class="mt-5 mb-5"></v-divider>

          <v-card-subtitle>Deep tagging results</v-card-subtitle>

          <!-- 속성들 -->
          <v-list-item v-for="(attribute,index) in attributes.text" :key="index">
            <v-list-item-action class="mr-2">
              <v-icon>mdi-chevron-right</v-icon>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-subtitle>{{ attribute.key }} : {{ attribute.values.join(', ') }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-card>
      </v-tab-item>
      <!-- Image tagging -->
      <v-tab-item>
        <v-card
          outlined
          class="pb-5"
        >
          <v-img
            width="900"
            :src="returnImageUrl(product.image)"
          >
          </v-img>          
          <v-card-actions class="justify-end">
            <v-btn
              color="primary"
              large
              @click="imageDeepTagging"
            >
              DEEP TAGGING
            </v-btn>
          </v-card-actions>

          <v-divider class="mt-5 mb-5"></v-divider>

          <v-card-subtitle>Deep tagging results</v-card-subtitle>

          <v-list-item v-for="(attribute,index) in attributes.image" :key="index">
            <v-list-item-action class="mr-2">
              <v-icon>mdi-chevron-right</v-icon>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-subtitle>{{ attribute.key }} : {{ attribute.values.join(', ') }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    product: {},
    htmlDescription: null,
    tab: {
      selected: null,
      titles: [
        'Detail',
        'Text deep tagging',
        'Image deep tagging',
      ],
    },
    attributes: {
      text: [],
      image: [],
    }

  }),
  created() {
    this.fetchProduct();
  },
  methods: {
    fetchProduct() {
      console.log('View - fetchProduct - params', this.$route.params.product_id);
      this.$store.dispatch('FETCH_PRODUCT', this.$route.params.product_id)
        .then(res => {
          console.log('View - fetchProduct - res', res);
          this.product = res;
          this.htmlDescription = this.product.description.replace(/(?:\r\n|\r|\n)/g, '<br/>');
        })
        .catch(error => { console.log(error) });
    },
    textDeepTagging() {
      this.$store.dispatch('INFER_TEXT', {name: this.product.name, description: this.product.description})
        .then(res => {
          console.log('View - textDeepTagging - res', res);
          this.attributes.text = res;
        })
        .catch(error => { console.log(error) });
    },
    imageDeepTagging() {
      this.$store.dispatch('INFER_IMAGE', {image: this.product.image})
        .then(res => {
          console.log('View - imageDeepTagging - res', res);
          this.attributes.image = res;
        })
        .catch(error => { console.log(error) });
    },

  },

}
</script>
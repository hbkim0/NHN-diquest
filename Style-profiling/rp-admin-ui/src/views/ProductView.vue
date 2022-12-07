<template>
  <v-card>
    <v-card-title><strong>Product</strong></v-card-title>
    <v-container row fluid class="mx-1">
      <v-col cols="auto">
        <v-text-field
          outlined
          clearable
          hide-details
          label="identifier"
          type="number"
          hide-spin-buttons
          append-icon="mdi-magnify"
          v-model="filter.selected.identifier"
          @input="debounceFunc.fetchProducts"
        >
        </v-text-field>
      </v-col>
      <v-col cols="auto">
        <v-select
          outlined
          clearable
          hide-details
          :items="filter.gender"
          v-model="filter.selected.gender"
          label="Gender"
          @change="debounceFunc.fetchProducts"
        ></v-select>
      </v-col>
      <v-col cols="auto">
        <v-select
          outlined
          clearable
          hide-details
          :items="filter.labels"
          v-model="filter.selected.label"
          label="Label"
          @change="debounceFunc.fetchProducts"
        ></v-select>
      </v-col>
      <v-col cols="auto">
        <v-autocomplete
          v-model="filter.selected.name"
          :items="filter.name"
          outlined
          clearable
          hide-details
          label="Name"
          @input="debounceFunc.fetchProducts"
          @update:search-input="debounceFunc.fetchAutocomplete($event)"
        ></v-autocomplete>
      </v-col>
    </v-container>
    <v-container row fluid class="mx-1">
      <v-col>
        <v-card 
          outlined 
          rounded
          elevation="2"
        >
          <v-simple-table
            fixed-header
          >
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-center text-subtitle-1">
                    <strong>identifier</strong>
                  </th>
                  <th class="text-center text-subtitle-1">
                    <strong>Label</strong>
                  </th>
                  <th class="text-center text-subtitle-1">
                    <strong>Gender</strong>
                  </th>
                  <th class="text-center text-subtitle-1">
                    <strong>Name</strong>
                  </th>
                  <th class="text-center text-subtitle-1">
                    
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="product in products"
                  :key="product._id"
                >
                  <td width="150" class="text-center">{{ product.identifier }}</td>
                  <td class="text-center">{{ product.label }}</td>
                  <td class="text-center">{{ product.gender }}</td>
                  <td class="text-center">{{ product.name }}</td>
                  <td class="text-center">
                    <v-btn
                      icon
                      :to="{ name: 'ProductDetailView', params: { product_id: product._id } }"
                    >
                      <v-icon
                      >
                        mdi-clipboard-text-outline
                      </v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
      </v-col>
    </v-container>
    <v-row>
      <v-col cols="11">
          <v-pagination
              v-model="pagenation.page"
              :length="pagenation.length"
              :total-visible="10"
              @input="fetchProducts"
          ></v-pagination>
      </v-col>
      <v-col cols="1" class="pr-10">
          <v-select
              v-model="filter.selected.limit"
              :items="[50,100,200,500]"
              dense
              outlined
              hint="per page"
              persistent-hint
              @change="fetchProducts"
          ></v-select>
      </v-col>   
    </v-row>
  </v-card>
</template>

<script>
import debounce from 'lodash/debounce';
import { mapGetters } from 'vuex';
export default {
  data: () => ({
    products: [],   
    filter: {
      gender: [
        { text: '남성', value: '남성' },
        { text: '여성', value: '여성' },
        { text: '혼성', value: '혼성' },
      ],
      labels: [],
      name: [],
      selected: {
        identifier: null,
        gender: null,
        label: null,
        name: null,
        limit: 50,
      }
    },
    pagenation: {
      page : 1,
      length : 0,
    },
    debounceFunc: {
      fetchProducts: null,
      fetchAutocomplete: null,
    },
  }),
  computed: {
    ...mapGetters({
      fetchedProductViewFilter: 'fetchedProductViewFilter',
    })
  },
  created() {
    //필터 유지
    if(this.$route.params.filterMaintain){
      this.filter.selected = this.fetchedProductViewFilter;
    }

    this.debounceFunc.fetchProducts = debounce(this.fetchProducts, 2000);
    this.debounceFunc.fetchAutocomplete = debounce(this.fetchAutocomplete, 700);
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      //
      this.filter.selected.identifier = this.filter.selected.identifier === "" ? null : this.filter.selected.identifier;

      const params = {...this.filter.selected, ...this.pagenation};
      console.log('View - fetchProducts - params', params);
      this.$store.dispatch('FETCH_PRODUCTS', params)
        .then(res => {
          console.log('View - fetchProducts - res', res);
          this.pagenation = res.pagenation;
          this.filter.selected.limit = res.limit;
          this.products = res.products;
          this.filter.labels = res.labels;
        })
        .catch(error => { console.log(error) });
    },
    fetchAutocomplete(name) {
      //FETCH_AUTOCOMPLETE
      this.$store.dispatch('FETCH_AUTOCOMPLETE', name)
        .then(res => {
          console.log('View - fetchAutocomplete - res', res);
          this.filter.name = res;
        })
        .catch(error => { console.log(error) });
    }
  }
}
</script>
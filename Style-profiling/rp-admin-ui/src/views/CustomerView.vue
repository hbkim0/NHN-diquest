<template>
  <v-card>
    <v-card-title><strong>Customer</strong></v-card-title>
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
          @input="debounceFunc.fetchCustomers"
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
          @input="debounceFunc.fetchCustomers"
        ></v-select>
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
                    <strong>Gender</strong>
                  </th>
                  <th class="text-center text-subtitle-1">
                    <strong>Zip Code</strong>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="customer in customers"
                  :key="customer.identifier"
                >
                  <td class="text-center">{{ customer.identifier }}</td>
                  <td class="text-center">{{ customer.gender }}</td>
                  <td class="text-center">{{ customer.zip_code }}</td>
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
          @input="fetchCustomers"
        ></v-pagination>
      </v-col>
      <v-col cols="1" class="pr-10">
        <v-select
          v-model="pagenation.limit"
          :items="[50,100,200,500]"
          dense
          outlined
          hint="per page"
          persistent-hint
          @change="fetchCustomers"
        ></v-select>
      </v-col>   
    </v-row>
  </v-card>
</template>

<script>
import debounce from 'lodash/debounce';
export default {
  data: () => ({
    customers: [],
    filter: {
      gender: [
        { text: '남성', value: '남성' },
        { text: '여성', value: '여성' },
      ],
      selected: {
        identifier: null,
        gender: null,
      }
    },
    pagenation: {
      page : 1,
      length : 0,
      limit: 50,
    },
    debounceFunc: {
      fetchCustomers: null,
    }
  }),
  created() {
    this.debounceFunc.fetchCustomers = debounce(this.fetchCustomers, 2000);
    this.fetchCustomers();
  },
  methods: {
    fetchCustomers() {
      //
      this.filter.selected.identifier = this.filter.selected.identifier === "" ? null : this.filter.selected.identifier;

      const params = {...this.filter.selected, ...this.pagenation};
      console.log('View - fetchCustomers - params', params);
      this.$store.dispatch('FETCH_CUSTOMERS', params)
        .then(res => {
          console.log('View - fetchCustomers - res', res);
          this.pagenation = res.pagenation;
          this.customers = res.customers;
        })
        .catch(error => { console.log(error) });
    }
  }
}
</script>
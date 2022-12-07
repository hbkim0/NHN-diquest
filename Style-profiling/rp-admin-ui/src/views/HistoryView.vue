<template>
  <v-card>
    <v-card-title><strong>History</strong></v-card-title>
    <v-container row fluid class="mx-1">
      <v-col cols="auto">
        <v-text-field
          outlined
          clearable
          hide-details
          label="Customer"
          type="number"
          hide-spin-buttons
          append-icon="mdi-magnify"
          v-model="filter.selected.customer"
          @input="debounceFunc.fetchHistories"
        >
        </v-text-field>
      </v-col>
      <v-col cols="auto">
        <v-text-field
          outlined
          clearable
          hide-details
          label="Product"
          type="number"
          hide-spin-buttons
          append-icon="mdi-magnify"
          v-model="filter.selected.product"
          @input="debounceFunc.fetchHistories"
        >
        </v-text-field>
      </v-col>
      <v-col cols="auto">
        <v-menu
            v-model="date.picker.start"
            :close-on-content-click="false"
            :nudge-right="40"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                outlined
                hide-details
                v-model="filter.selected.startDate"
                label="StartDate"
                prepend-inner-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="filter.selected.startDate"
              :max="filter.selected.endDate"
              @input="date.picker.start = false;debounceFunc.fetchHistories();"
            ></v-date-picker>
          </v-menu>
      </v-col>
      <v-col cols="auto" class="align-center">
        <v-card-text class="mx-1 text-h6 pl-0 pr-0">~</v-card-text>
      </v-col>
      <v-col cols="auto">
        <v-menu
            v-model="date.picker.end"
            :close-on-content-click="false"
            :nudge-right="40"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                outlined
                hide-details
                v-model="filter.selected.endDate"
                label="EndDate"
                prepend-inner-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="filter.selected.endDate"
              @input="date.picker.end = false;debounceFunc.fetchHistories();"
            ></v-date-picker>
          </v-menu>
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
                    <strong>Customer</strong>
                  </th>
                  <th class="text-center text-subtitle-1">
                    <strong>Product</strong>
                  </th>
                  <th class="text-center text-subtitle-1">
                    <strong>Rating</strong>
                  </th>
                  <th class="text-center text-subtitle-1">
                    <strong>Rating Time</strong>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="history in histories"
                  :key="history._id"
                >
                  <td class="text-center">{{ history.customer }}</td>
                  <td class="text-center">{{ history.product }}</td>
                  <td class="text-center">{{ history.rating }}</td>
                  <td class="text-center">{{ dayjs(history.reg_date).format('YYYY-MM-DD hh:mm:ss') }}</td>
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
              @input="fetchHistories"
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
              @change="fetchHistories"
          ></v-select>
      </v-col>   
    </v-row>
  </v-card>
</template>

<script>
import debounce from 'lodash/debounce';
export default {
  data: () => ({
    histories: [],
    date: {
      picker: {
        start : false,
        end: false,
      },
    },
    filter: {
      selected: {
        customer: null,
        product: null,
        startDate: null,
        endDate: null,
      }
    },
    pagenation: {
      page : 1,
      length : 0,
      limit: 50,
    },
    debounceFunc: {
      fetchHistories: null,
    },
  }),
  created() {
    this.debounceFunc.fetchHistories = debounce(this.fetchHistories, 2000);
    this.filter.selected.endDate = this.dayjs().format('YYYY-MM-DD');
    this.filter.selected.startDate = this.dayjs().startOf('month').format('YYYY-MM-DD');
    this.fetchHistories();
  },
  methods: {
    fetchHistories() {
      //
      this.filter.selected.customer = this.filter.selected.customer === "" ? null : this.filter.selected.customer;
      this.filter.selected.product = this.filter.selected.product === "" ? null : this.filter.selected.product;

      const params = {...this.filter.selected, ...this.pagenation};
      console.log('View - fetchHistories - params', params);
      this.$store.dispatch('FETCH_HISTORIES', params)
        .then(res => {
          console.log('View - fetchHistories - res', res);
          this.pagenation = res.pagenation;
          this.histories = res.histories;
        })
        .catch(error => { console.log(error) });
    }
  }
}
</script>
<template>
  <v-container fluid>
    <v-card>
      <v-card-title><strong>Dataset inflow history</strong></v-card-title>
      <v-container class="pa-0 ma-0" row fluid>
        <v-col cols="auto ml-10">
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
                v-model="date.startDate"
                label="StartDate"
                prepend-inner-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="date.startDate"
              :max="date.endDate"
              @input="date.picker.start = false;debounceFunc.fetchStatus();"
            ></v-date-picker>
          </v-menu>
        </v-col>
        <v-col cols="auto" class="align-center">
          <v-card-text class="mx-1 text-h6 px-0">~</v-card-text>
        </v-col>
        <v-col cols="auto mx-1">
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
                v-model="date.endDate"
                label="EndDate"
                prepend-inner-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="date.endDate"
              :min="date.startDate"
              @input="date.picker.end = false;debounceFunc.fetchStatus();"
            ></v-date-picker>
          </v-menu>
        </v-col>
        <v-col cols="auto">
          <v-btn
            x-large
            color="white"
            class="blue--text"
            @click="dateRangeWeek"
          >
            WEEK
          </v-btn>
        </v-col>
        <v-col>
          <v-btn
            x-large
            color="white"
            class="blue--text"
            @click="dateRangeMonth"
          >
            MONTH
          </v-btn>
        </v-col>
      </v-container>

      <v-row justify="center">
        <v-col>
          <v-card class="pa-3 ml-10 mr-10">
            <v-card-title>Total</v-card-title>
            <LineChart
              :chart-data="chart.lineChartData"
            ></LineChart>
          </v-card>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col>
          <v-card class="pa-3 ml-10 mr-10">
            <v-card-title>Differential</v-card-title>
            <BarChart
              :chart-data="chart.barChartData"
            ></BarChart>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
import BarChart from '../components/BarChart.vue';
import LineChart from '../components/LineChart.vue';
import debounce from 'lodash/debounce';
export default {
  components: {
    BarChart,
    LineChart,
  },
  data: () => ({
    date: {
      picker: {
        start : false,
        end: false,
      },
      startDate: null,
      endDate: null,
    },
    chart: {
      barChartData: {},
      lineChartData: {},
    },
    debounceFunc: {
      fetchStatus: null,
    },
    lineChartPointer: {
      pointStyle: 'circle',
      pointRadius: 6,
      fill: false,
    }
  }),
  created() {
    this.debounceFunc.fetchStatus = debounce(this.fetchStatus, 2000);
    this.date.endDate = this.dayjs().format('YYYY-MM-DD');
    this.date.startDate = this.dayjs().startOf('month').format('YYYY-MM-DD');
    this.fetchStatus();
  },
  methods: {
    dateRangeWeek() {
      const date = this.dayjs(this.date.endDate);
      this.date.startDate = date.subtract(7, 'day').format('YYYY-MM-DD');
      this.fetchStatus();
    },
    dateRangeMonth() {
      const date = this.dayjs(this.date.endDate);
      this.date.startDate = date.subtract(1, 'month').format('YYYY-MM-DD');
      this.fetchStatus();
    },
    fetchStatus() {
      this.$store.dispatch('FETCH_STATUS', {start: this.date.startDate, end: this.date.endDate})
        .then(res => {
          //console.log('View - fetchStatus - res', res);
          const labels = res.map(obj => obj.date);
          this.chart.lineChartData = {
            labels,
            datasets: [
              { label: 'customer', data: res.map(obj => obj.customer.total), backgroundColor: '#6666CC', borderColor: '#6666CC', ...this.lineChartPointer },
              { label: 'product', data: res.map(obj => obj.product.total), backgroundColor: '#FF9999', borderColor: '#FF9999', ...this.lineChartPointer },
              { label: 'history', data: res.map(obj => obj.history.total), backgroundColor: '#EEEECC', borderColor: '#EEEECC', ...this.lineChartPointer },
            ]
          }

          this.chart.barChartData = {
            labels,
            datasets: [
              { label: 'customerIn', data: res.map(obj => obj.customer.in), stack: 'customer', backgroundColor: '#6666CC' },
              { label: 'customerOut', data: res.map(obj => obj.customer.out), stack: 'customer', backgroundColor: '#FF9999' },
              { label: 'productIn', data: res.map(obj => obj.product.in), stack: 'product', backgroundColor: '#EEEECC' },
              { label: 'productOut', data: res.map(obj => obj.product.out), stack: 'product', backgroundColor: '#333366' },
              { label: 'historyIn', data: res.map(obj => obj.history.in), stack: 'history', backgroundColor: '#993333' },
              { label: 'historyOut', data: res.map(obj => obj.history.out), stack: 'history', backgroundColor: '#FFFF99' },
            ]
          }
        })
        .catch(error => { console.log(error) });
    },
  }
}
</script>
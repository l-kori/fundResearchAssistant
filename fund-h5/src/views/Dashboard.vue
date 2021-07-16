<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-6">
      <div class="row">
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="基金指数"
            type="gradient-red"
            :sub-title="jjjz"
            icon="ni ni-active-40"
            class="mb-4 mb-xl-0"
          >
            <template v-slot:footer>
              <i
              class="fas mr-3"
              :class="
                 jjzf >= 0
                  ? 'text-danger fa-arrow-up'
                  : 'text-success fa-arrow-down'
              "
            >{{ jjzf }}%
            </i>
            </template>
          </stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="上证指数"
            type="gradient-orange"
            :sub-title="szjz"
            icon="ni ni-chart-pie-35"
            class="mb-4 mb-xl-0"
          >
            <template v-slot:footer>
              <i
              class="fas mr-3"
              :class="
                 szzf >= 0
                  ? 'text-danger fa-arrow-up'
                  : 'text-success fa-arrow-down'
              "
            >{{ szzf }}%
            </i>
            </template>
          </stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="深证成指"
            type="gradient-green"
            :sub-title="szczjz"
            icon="ni ni-money-coins"
            class="mb-4 mb-xl-0"
          >
            <template v-slot:footer>
              <i
              class="fas mr-3"
              :class="
                 szczzf >= 0
                  ? 'text-danger fa-arrow-up'
                  : 'text-success fa-arrow-down'
              "
            >{{ szczzf }}%
            </i>
            </template>
          </stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="创业板指"
            type="gradient-info"
            :sub-title="cybjj"
            icon="ni ni-chart-bar-32"
            class="mb-4 mb-xl-0"
          >
            <template v-slot:footer>
              <i
              class="fas mr-3"
              :class="
                 cybzf >= 0
                  ? 'text-danger fa-arrow-up'
                  : 'text-success fa-arrow-down'
              "
            >{{ cybzf }}%
            </i>
            </template>
          </stats-card>
        </div>
      </div>
    </base-header>

    <div class="container-fluid mt--7">
      <!--Charts-->
      <div class="row">
        <div class="col-xl-12 mb-5 mb-xl-0">
          <card type="default" header-classes="bg-transparent">
            <template v-slot:header>
              <div class="row align-items-center">
                <div class="col">
                  <h5 class="h3 text-white mb-0">单位净值</h5>
                </div>
                <div class="col">
                  <!-- <ul class="nav nav-pills justify-content-end">
                    <li class="nav-item mr-2 mr-md-0">
                      <a
                        class="nav-link py-2 px-3"
                        href="#"
                        :class="{ active: bigLineChart.activeIndex === 0 }"
                        @click.prevent="initBigChart(0)"
                      >
                        <span class="d-none d-md-block">Month</span>
                        <span class="d-md-none">M</span>
                      </a>
                    </li>
                    <li class="nav-item">
                      <a
                        class="nav-link py-2 px-3"
                        href="#"
                        :class="{ active: bigLineChart.activeIndex === 1 }"
                        @click.prevent="initBigChart(1)"
                      >
                        <span class="d-none d-md-block">Week</span>
                        <span class="d-md-none">W</span>
                      </a>
                    </li>
                  </ul> -->
                </div>
              </div>
            </template>
            <div class="chart-area">
              <canvas :height="350" :id="salesChartID"></canvas>
            </div>
          </card>
        </div>
      </div>
      <!-- End charts-->

      <!--Tables-->
      <div class="row mt-5">
        <div class="col-xl-8 mb-5 mb-xl-0">
          <page-visits-table></page-visits-table>
        </div>
        <div class="col-xl-4">
          <social-traffic-table></social-traffic-table>
        </div>
      </div>
      <!--End tables-->
    </div>
  </div>
</template>
<script>
import Chart from "chart.js";

import PageVisitsTable from "./Dashboard/PageVisitsTable";
import SocialTrafficTable from "./Dashboard/SocialTrafficTable";
import axios from "axios";
let chart;

export default {
  components: {
    PageVisitsTable,
    SocialTrafficTable,
  },
  data() {
    return {
      salesChartID: "salesChart",
      // ordersChartID: "ordersChart",
      bigLineChart: {
        allData: [
          [
            0, 20, 10, 30, 15, 40, 20, 60, 60, 15, 40, 20, 60, 60, 15, 40, 20,
            60, 60,
          ],
          [0, 20, 5, 25, 10, 30, 15, 40, 40],
        ],
        activeIndex: 0,
      },
      jjjz: "909,099",
      jjzf: "-",
      szjz: "-",
      szzf: "-",
      szczjz: "-",
      szczzf: "-",
      cybjj: "-",
      cybzf: "-",
    };
  },

  methods: {
    // 基金
    getjjzsValue() {
      axios({
        url: "http://push2.eastmoney.com/api/qt/stock/get?secid=1.000011&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f118,f107,f57,f58,f59,f152,f43,f169,f170,f46,f60,f44,f45,f168,f50,f47,f48,f49,f46,f169,f161,f117,f85,f47,f48,f163,f171,f113,f114,f115,f86,f117,f85,f119,f120,f121,f122,f292&invt=2&_=1626235093935",
        method: "get",
      }).then((response) => {
        // 上证净值
        const jjjz = response.data.data["f43"] / 100;
        // 上证昨收
        const jjzs = response.data.data["f60"] / 100;
        // 计算涨幅
        const jjzf = (((jjjz - jjzs) / jjzs) * 100).toFixed(2);
        this.jjjz = jjjz;
        this.jjzf = jjzf;
      }),
        (err) => {
          console.log(err);
        };
    },
    // 上证
    getszzsValue() {
      axios({
        url: "http://push2.eastmoney.com/api/qt/stock/get?secid=1.000001&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f118,f107,f57,f58,f59,f152,f43,f169,f170,f46,f60,f44,f45,f168,f50,f47,f48,f49,f46,f169,f161,f117,f85,f47,f48,f163,f171,f113,f114,f115,f86,f117,f85,f119,f120,f121,f122,f292&invt=2&_=1626235093935",
        method: "get",
      }).then((response) => {
        // 上证净值
        const jjjz = response.data.data["f43"] / 100;
        // 上证昨收
        const jjzs = response.data.data["f60"] / 100;
        // 计算涨幅
        const jjzf = (((jjjz - jjzs) / jjzs) * 100).toFixed(2);
        this.szjz = jjjz;
        this.szzf = jjzf;
      }),
        (err) => {
          console.log(err);
        };
    },
    // 深证
    getszczValue() {
      axios({
        url: "http://push2.eastmoney.com/api/qt/stock/get?secid=0.399001&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f118,f107,f57,f58,f59,f152,f43,f169,f170,f46,f60,f44,f45,f168,f50,f47,f48,f49,f46,f169,f161,f117,f85,f47,f48,f163,f171,f113,f114,f115,f86,f117,f85,f119,f120,f121,f122,f292&invt=2&_=1626235093935",
        method: "get",
      }).then((response) => {
        // 上证净值
        const jjjz = response.data.data["f43"] / 100;
        // 上证昨收
        const jjzs = response.data.data["f60"] / 100;
        // 计算涨幅
        const jjzf = (((jjjz - jjzs) / jjzs) * 100).toFixed(2);
        // console.log(jjjz, jjzf);
        this.szczjz = jjjz;
        this.szczzf = jjzf;
      }),
        (err) => {
          console.log(err);
        };
    },
    // 创业板
    getcybValue() {
      axios({
        url: "http://push2.eastmoney.com/api/qt/stock/get?secid=0.395004&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f118,f107,f57,f58,f59,f152,f43,f169,f170,f46,f60,f44,f45,f168,f50,f47,f48,f49,f46,f169,f161,f117,f85,f47,f48,f163,f171,f113,f114,f115,f86,f117,f85,f119,f120,f121,f122,f292&invt=2&_=1626235093935",
        method: "get",
      }).then((response) => {
        // 上证净值
        const jjjz = response.data.data["f43"] / 100;
        // 上证昨收
        const jjzs = response.data.data["f60"] / 100;
        // 计算涨幅
        const jjzf = (((jjjz - jjzs) / jjzs) * 100).toFixed(2);
        this.cybjj = jjjz;
        this.cybzf = jjzf;
      }),
        (err) => {
          console.log(err);
        };
    },
    initBigChart(index) {
      chart.destroy();
      chart = new Chart(
        document.getElementById(this.salesChartID).getContext("2d"),
        {
          type: "line",
          data: {
            labels: [
              "May",
              "Jun",
              "Jul",
              "Aug",
              "Sep",
              "Oct",
              "Nov",
              "Dec",
              "Jun",
              "Jul",
              "Aug",
              "Sep",
              "Oct",
              "Nov",
              "Dec",
              "Jun",
              "Jul",
              "Aug",
              "Sep",
              "Oct",
              "Nov",
              "Dec",
            ],
            datasets: [
              {
                label: "Performance",
                tension: 0.4,
                borderWidth: 4,
                borderColor: "#5e72e4",
                pointRadius: 0,
                backgroundColor: "transparent",
                data: this.bigLineChart.allData[index],
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
              display: false,
            },
            tooltips: {
              enabled: true,
              mode: "index",
              intersect: false,
            },
            scales: {
              yAxes: [
                {
                  barPercentage: 1.6,
                  gridLines: {
                    drawBorder: false,
                    color: "rgba(29,140,248,0.0)",
                    zeroLineColor: "transparent",
                  },
                  ticks: {
                    padding: 0,
                    fontColor: "#8898aa",
                    fontSize: 13,
                    fontFamily: "Open Sans",
                  },
                },
              ],
              xAxes: [
                {
                  barPercentage: 1.6,
                  gridLines: {
                    drawBorder: false,
                    color: "rgba(29,140,248,0.0)",
                    zeroLineColor: "transparent",
                  },
                  ticks: {
                    padding: 10,
                    fontColor: "#8898aa",
                    fontSize: 13,
                    fontFamily: "Open Sans",
                  },
                },
              ],
            },
            layout: {
              padding: 0,
            },
          },
        }
      );
      this.bigLineChart.activeIndex = index;
    },
  },
  mounted() {
    //定时请求大盘
    const that = this;
    that.getjjzsValue();
    that.getszzsValue();
    that.getszczValue();
    that.getcybValue();
    that.timer = setInterval(function () {
      that.getjjzsValue();
      that.getszzsValue();
      that.getszczValue();
      that.getcybValue();
    }, 12000);
    chart = new Chart(
      document.getElementById(this.salesChartID).getContext("2d"),
      {
        type: "line",
        data: {
          labels: [
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
          ],
          datasets: [
            {
              label: "Performance",
              tension: 0.4,
              borderWidth: 4,
              borderColor: "#5e72e4",
              pointRadius: 0,
              backgroundColor: "transparent",
              data: this.bigLineChart.allData[1],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          legend: {
            display: false,
          },
          tooltips: {
            enabled: true,
            mode: "index",
            intersect: false,
          },
          scales: {
            yAxes: [
              {
                barPercentage: 1.6,
                gridLines: {
                  drawBorder: false,
                  color: "rgba(29,140,248,0.0)",
                  zeroLineColor: "transparent",
                },
                ticks: {
                  padding: 0,
                  fontColor: "#8898aa",
                  fontSize: 13,
                  fontFamily: "Open Sans",
                },
              },
            ],
            xAxes: [
              {
                barPercentage: 1.6,
                gridLines: {
                  drawBorder: false,
                  color: "rgba(29,140,248,0.0)",
                  zeroLineColor: "transparent",
                },
                ticks: {
                  padding: 10,
                  fontColor: "#8898aa",
                  fontSize: 13,
                  fontFamily: "Open Sans",
                },
              },
            ],
          },
          layout: {
            padding: 0,
          },
        },
      }
    );
    // ordersChart.createChart(this.ordersChartID);
  },
};
</script>
<style></style>

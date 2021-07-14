<template>
  <div class="card">
    <div class="card-header border-0">
      <div class="row align-items-center">
        <div class="col">
          <h2 class="mb-0">我的自选</h2>
        </div>
        <!-- <div class="col text-right">
          <a href="#!" class="btn btn-sm btn-primary">See all</a>
        </div> -->
      </div>
    </div>

    <div class="table-responsive" id="app">
      <base-table thead-classes="thead-light" :data="tableData">
        <template v-slot:columns>
          <th>基金名称</th>
          <th>代码</th>
          <th>净值</th>
          <th>估值</th>
          <th>涨幅</th>
        </template>

        <template v-slot:default="row">
          <th scope="row">
            {{ row.item.name }}
          </th>
          <td>
            {{ row.item.fundcode }}
          </td>
          <td>
            {{ row.item.dwjz }}
          </td>
          <td>
            {{ row.item.gsz }}
          </td>
          <td>
            {{ row.item.gszzl }}
            <i
              class="fas mr-3"
              :class="
                row.item.gszzl >= 0
                  ? 'text-danger fa-arrow-up'
                  : 'text-success fa-arrow-down'
              "
            >
            </i>
          </td>
        </template>
      </base-table>
    </div>
  </div>
</template>
<!--<script src="https://unpkg.com/axios/dist/axios.min.js"></script>-->

<script>
import axios from "axios";
export default {
  name: "page-visits-table",
  data() {
    
    return {
      tableData: [],
    };
  },
  
  mounted() {
    const that = this;
    that.getList();
    that.timer = setInterval(function () {
      that.getList()
    }, 120000);
  },
  methods: {
    getList() {
      axios({
        url: "http://localhost:8000/userlivedata",
        method: "get",
        params: {
          account: "lxd",
        },
      }).then((response) => {
        this.tableData = response.data.data;
      }),
        (err) => {
          console.log(err);
        };
    }
  },
};
</script>
<style></style>

<template>
  <div class="card">
    <div class="card-header border-0">
      <div class="row align-items-center">
        <div class="col">
          <h3 class="mb-0">热门基金排行榜</h3>
        </div>
        <!-- <div class="col text-right">
          <base-button size="sm" type="primary">See all</base-button>
        </div> -->
      </div>
    </div>

    <div class="table-responsive">
      <base-table thead-classes="thead-light" :data="tableData">
        <template v-slot:columns>
          <th>基金名称</th>
          <th>涨幅</th>
        </template>

        <template v-slot:default="row">
          <th scope="row">
            {{ row.item.name }}
          </th>
          <td>
            {{ row.item.zf }}
            <i
              class="fas mr-3"
              :class="
                row.item.zf >= 0
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
<script>
export default {
  name: "social-traffic-table",
  data() {
    return {
      tableData: [
        {
          name: "Facebook",
          zf:'60',
        }
      ],
    };
  },
};
</script>
<style></style>

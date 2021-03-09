<template>
  <div>
    <div class="sub-title">{{this.$route.params.name}}</div>
    <bk-divider></bk-divider>
    <div>
      <bk-button theme="primary">新建</bk-button>
      <bk-input placeholder="搜索" right-icon="bk-icon icon-search" style="width: 308px;float:right;"></bk-input>
    </div>
    <bk-table style="margin-top: 15px;" :data="ciData" :size="setting.size">
      <bk-table-column v-for="field in setting.selectedFields" :key="field.id" :label="field.label" :prop="field.id">
      </bk-table-column>
      <bk-table-column type="setting">
        <bk-table-setting-content :fields="setting.fields" :selected="setting.selectedFields" :max="setting.max" :size="setting.size"
          @setting-change="handleSettingChange">
        </bk-table-setting-content>
      </bk-table-column>
    </bk-table>
    <bk-pagination size="small" :current.sync="pagingConfigTwo.current" :limit="pagingConfigTwo.limit" :count="pagingConfigTwo.count"
      :location="pagingConfigTwo.location" :align="pagingConfigTwo.align" :show-limit="pagingConfigTwo.showLimit"
      :limit-list="pagingConfigTwo.limitList" :show-total-count="pagingConfigTwo.totalCount" @change="changePage" @limit-change="changeLimit">
    </bk-pagination>
  </div>
</template>

<script>
import {
  getCI
} from '@/api/api'
export default {
  name: 'resources',
  data () {
    const fields = [{
      id: 'ci_id',
      label: '暂无数据'
    }]
    return {
      pk: this.$route.params.schemaID,
      ciData: [],
      setting: {
        max: 3,
        fields: fields,
        selectedFields: fields.slice(0, 3),
        size: 'small'
      },
      pagingConfigTwo: {
        current: 1,
        limit: 10,
        count: 0,
        location: 'left',
        align: 'right',
        showLimit: true,
        limitList: [10, 20, 50],
        totalCount: true
      }
    }
  },
  methods: {
    getCIData () {
      getCI(this.pk, {page: this.pagingConfigTwo.current, page_size: this.pagingConfigTwo.limit}).then((res) => {
        this.ciData = res.data.data.item
        this.pagingConfigTwo.count = res.data.data.count
        console.log(this.ciData)
      }).catch((err) => {
        console.log(err)
      })
    },
    handleSettingChange ({
      fields,
      size
    }) {
      this.setting.size = size
      this.setting.selectedFields = fields
    },
    changePage (page) {
      console.log(page)
      this.pagingConfigTwo.current = page
      this.getCIData()
    },
    changeLimit (limit) {
      this.pagingConfigTwo.limit = limit
      this.getCIData()
    }
  },
  mounted () {
    if (this.fieldList.length !== 0) {
      this.setting.fields = this.fieldList
      this.setting.selectedFields = this.fieldList
    }
    this.getCIData()
  },
  computed: {
    fieldList () {
      var index
      var fields = []
      for (index in this.$route.params.fields) {
        fields.push({
          id: this.$route.params.fields[index].name,
          label: this.$route.params.fields[index].alias
        })
      }
      return fields
    }
  }
}
</script>

<style>
  .sub-title {
    font-size: 20px;
    margin-left: 12px;
    margin: 14px;
    height: 23px;
  }
</style>

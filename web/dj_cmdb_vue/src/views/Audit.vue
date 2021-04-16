<template>
  <div>
    <div class="sub-title">操作审计</div>
    <bk-divider></bk-divider>
    <div style="margin-left: 10px;margin-right: 10px;">
      <bk-input placeholder="搜索" right-icon="bk-icon icon-search" style="width: 308px;float:right;"></bk-input>
    </div>
    <bk-table style="margin-top: 15px;" :data="auditData" :size="setting.size">
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
      :limit-list="pagingConfigTwo.limitList" :show-total-count="pagingConfigTwo.totalCount" @change="changePage"
      @limit-change="changeLimit">
    </bk-pagination>
  </div>
</template>

<script>
import {getAudit} from '@/api/api'
export default {
  data () {
    const fields = [{
      id: 'user',
      label: '操作者'
    },
    {
      id: 'obj',
      label: '操作对象'
    },
    {
      id: 'operate_type',
      label: '操作动作'
    },
    {
      id: 'change_message',
      label: '操作描述'
    },
    {
      id: 'action_time',
      label: '操作时间'
    }
    ]
    return {
      auditData: [],
      setting: {
        max: 3,
        fields: fields,
        selectedFields: fields.slice(0, 4),
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
  mounted () {
    this.getAuditData()
  },
  methods: {
    handleSettingChange ({
      fields,
      size
    }) {
      this.setting.size = size
      this.setting.selectedFields = fields
    },
    changePage (page) {
      this.pagingConfigTwo.current = page
      this.getSub()
    },
    changeLimit (limit) {
      this.pagingConfigTwo.limit = limit
      this.getSub()
    },
    getAuditData () {
      getAudit({
        page: this.pagingConfigTwo.current,
        page_size: this.pagingConfigTwo.limit
      }).then((res) => {
        this.auditData = res.data.data.items
      }).catch((err) => {
        console.log(err)
      })
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

<template>
  <div>
    <div style="font-size: 20px;margin-left: 12px;margin: 14px;">关联关系</div>
    <bk-divider></bk-divider>
    <bk-container flex :col="12">
      <bk-row>
        <bk-col :span="4">
          <bk-button @click="createRelationSettings.visible = true" :theme="'primary'" :title="'新建关系'" class="mr10">
            新建关系
          </bk-button>
          <bk-dialog v-model="createRelationSettings.visible" title="新建关系" :header-position="createRelationSettings.headerPosition"
            :width="createRelationSettings.width" @confirm="postCiRelation">
            <div>唯一标识</div>
            <bk-input :placeholder="'请输入唯一标识'" style="margin-bottom: 15px;" v-model="postRelationData.name">
            </bk-input>
            <div>属性名称</div>
            <bk-input :placeholder="'请输入关系名称'" style="margin-bottom: 15px;" v-model="postRelationData.alias">
            </bk-input>
          </bk-dialog>
        </bk-col>
        <bk-col :span="4"></bk-col>
        <bk-col :span="4">
          <bk-row>
            <bk-input clearable :placeholder="'请输入关键字'" :right-icon="'bk-icon icon-search'" v-model="value"
              @right-icon-click="handlerIconClick">
            </bk-input>
          </bk-row>
        </bk-col>
      </bk-row>
    </bk-container>
    <div style="display: flex;width: 100%;flex-wrap: wrap;margin-top: 20px;margin-left: 20px;">
      <div v-for="(relation,index) in this.relationList" :key="'relation'+index" class="card-demo" style="width: 200px;height: 60px;" @click="customSettings.isShow = true">
        <bk-card title="卡片标题" :show-foot="false" :show-head="false" style="width: 100%;height: 100%;">
          <div style="display: flex;width: 100%;height: 100%;">
            <div style="margin-left: 26px;margin-top: auto;margin-bottom: auto;">
              <div style="color: darkgray;">{{relation.alias}}</div>
              <div style="display: flex;margin-top: 3px;">
                <div style="color: lightgray;font-size: 14px;">{{relation.name}}</div>
              </div>
            </div>
          </div>
        </bk-card>
      </div>
    </div>
  </div>
</template>

<script>
import {ciRelation, createCiRelation} from '@/api/api'
export default {
  name: 'relation',
  mounted () {
    this.getCiRelation()
  },
  data () {
    return {
      createRelationSettings: {
        visible: false,
        width: 480,
        headerPosition: 'left'
      },
      postRelationData: {
        name: '',
        alias: ''
      },
      value: '',
      relationList: []
    }
  },
  methods: {
    postCreateRelation () {
      console.log('1')
    },
    handlerIconClick () {
      console.log('1')
    },
    getCiRelation () {
      ciRelation().then((response) => {
        this.relationList = response.data.data
      }).catch((error) => {
        this.$bkMessage({
          theme: 'error',
          message: error.message
        })
      })
    },
    postCiRelation () {
      createCiRelation(this.postRelationData).then((response) => {
        this.getCiRelation()
        this.$bkMessage({
          theme: 'success',
          message: '创建成功'
        }).catch((error) => {
          this.$bkMessage({
            theme: 'error',
            message: error.message
          })
        })
      })
    }
  }
}
</script>

<style>
  .bk-card-body {
    width: 100%;
    height: 100%;
  }
</style>

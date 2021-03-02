<template>
  <div>
    <div style="font-size: 20px;margin-left: 12px;margin: 14px;">模型</div>
    <bk-divider></bk-divider>
    <div class="wrapper flex">
      <bk-container flex :col="12">
        <bk-row>
          <bk-col :span="4">
            <bk-button @click="createModelSettings.visible = true" :theme="'primary'" :title="'新建模型'" class="mr10">
              新建模型
            </bk-button>
            <bk-dialog v-model="createModelSettings.visible" title="新建模型" :header-position="createModelSettings.headerPosition"
              :width="createModelSettings.width" @confirm="postCreateModel">
              <div>所属分组</div>
              <bk-select :disabled="false" :search-with-pinyin="true" v-model="postModelData.group" style="width: 250px;" ext-cls="select-custom"
                ext-popover-cls="select-popover-custom" searchable>
                <bk-option v-for="item in this.groupList" :key="item.id" :id="item.id" :name="item.alias">
                </bk-option>
              </bk-select>
              <div>唯一标识</div>
              <bk-input :placeholder="'请输入唯一标识'" style="margin-bottom: 15px;" v-model="postModelData.name">
              </bk-input>
              <div>模型名称</div>
              <bk-input :placeholder="'请输入模型名称'" style="margin-bottom: 15px;" v-model="postModelData.alias">
              </bk-input>
            </bk-dialog>
            <bk-button @click="createGroupSettings.visible = true" :theme="'default'" :title="'新建分组'" class="mr10">
              新建分组
            </bk-button>
            <bk-dialog v-model="createGroupSettings.visible" title="新建分组" :header-position="createGroupSettings.headerPosition"
              :width="createGroupSettings.width" @confirm="postCreateGroup">
              <div>唯一标识</div>
              <bk-input :placeholder="'请输入唯一标识'" style="margin-bottom: 15px;" v-model="postGroupData.name">
              </bk-input>
              <div>分组名称</div>
              <bk-input :placeholder="'请输入分组名称'" style="margin-bottom: 15px;" v-model="postGroupData.alias">
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
    </div>
    <bk-collapse v-model="activeName">
      <div v-for="(group,index) in groupList" :key="'group'+index">
        <bk-collapse-item :name="group.id" class="ci-group">
          {{group.alias}}
          <div slot="content" class="f13">
            <div style="display: flex;width: 100%;flex-wrap: wrap;">
              <div v-for="(ci,index) in group.schema" :key="'ci'+index" class="card-demo">
                <bk-card title="卡片标题" :show-foot="false" :show-head="false" style="width: 100%;height: 100%;">
                  <div style="display: flex;" class="a-card">
                    <bk-icon type="pc" style="font-size: 36px;line-height: 72px;margin-left: 10px;color: #3A84FF;" />
                    <div style="margin-left: 26px;">
                      <p>{{ci.alias}}</p>
                      <p style="color: lightgray;">{{ci.name}}</p>
                    </div>
                    <bk-icon type="order" style="font-size: 24px;line-height: 64px;margin-left: 60px;" class="detail" />
                  </div>
                </bk-card>
              </div>
            </div>
          </div>
        </bk-collapse-item>
      </div>
    </bk-collapse>
  </div>
</template>

<script>
import {
  ciSChemaGroup,
  ciSChema,
  CreateSChemaGroup
} from '@/api/api'
export default {
  name: 'model-management',
  mounted () {
    this.getCiSchemaGroup()
  },
  data () {
    return {
      activeName: [],
      value: '',
      select_group: '',
      groupList: [],
      createModelSettings: {
        visible: false,
        width: 480,
        headerPosition: 'left'
      },
      createGroupSettings: {
        visible: false,
        width: 480,
        headerPosition: 'left'
      },
      postModelData: {
        group: '',
        name: '',
        alias: ''
      },
      postGroupData: {
        name: '',
        alias: ''
      }
    }
  },
  methods: {
    handlerIconClick () {
      console.log('1')
    },
    getCiSchemaGroup () {
      ciSChemaGroup().then((response) => {
        this.groupList = response.data.data
        var activeName = []
        var index
        for (index in this.groupList) {
          activeName.push(this.groupList[index].id)
        }
        this.activeName = activeName
      }).catch((error) => {
        console.log(error)
      })
    },
    postCreateModel () {
      ciSChema(this.postModelData).then((response) => {
        this.$bkMessage({theme: 'success', message: '创建成功'})
        this.getCiSchemaGroup()
      }).catch((error) => {
        this.$bkMessage({theme: 'error', message: error.message})
      })
    },
    postCreateGroup () {
      CreateSChemaGroup(this.postGroupData).then((response) => {
        this.$bkMessage({theme: 'success', message: '创建成功'})
        this.getCiSchemaGroup()
      }).catch((error) => {
        this.$bkMessage({theme: 'error', message: error.message})
      })
    }
  }
}
</script>

<style>
  .detail {
    display: none;
    transition: all.7s;
  }

  .detail:hover {
    color: skyblue;
  }

  .a-card:hover .detail {
    display: block;
    background: skyblue;
    flex: 1;
  }
</style>

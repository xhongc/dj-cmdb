<template>
  <div>
    <div style="font-size: 20px;margin-left: 12px;margin: 14px;">资源目录</div>
    <bk-divider></bk-divider>
    <div class="resource-menu">
      <div v-for="(schemaGroup,index) in schemaGroupList" :key="'schemaGroup'+index" class="card-demo">
        <bk-card :title="schemaGroup.alias">
          <div v-for="(schema,index) in schemaGroup.schema" :key="'schema'+index" class="field">
          <div>{{schema.alias}}</div>
          <bk-icon type="smile" class="smile-s"/>
          </div>
        </bk-card>
      </div>
    </div>
  </div>
</template>

<script>
import {
  ciSChemaGroup
} from '@/api/api'
export default {
  name: 'resource',
  mounted () {
    this.getCiSChemaGroup()
  },
  data () {
    return {
      schemaGroupList: []
    }
  },
  methods: {
    getCiSChemaGroup () {
      ciSChemaGroup().then((response) => {
        console.log('1')
        this.schemaGroupList = response.data.data
      }).catch((error) => {
        console.log('2', error)
      })
    }
  }
}
</script>

<style scoped>
  .card-demo {
    width: 200px;
    display: inline-block;
    float: left;
    margin-right: 10px;
    flex-direction: column;
  }
  .smile-s:hover {
    font-size: 64px;
    color: red;
  }
  .field {
    display: flex;
  }
  .resource-menu {
    display: flex;
    flex-direction: row;
    margin: 0 auto;
    width: 1;
  }
</style>

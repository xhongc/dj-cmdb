<template>
  <div style="height: 100%;">
    <div style="font-size: 20px;margin-left: 12px;margin: 14px;">关系拓扑图</div>
    <bk-divider></bk-divider>
    <div id="topoTree"></div>
  </div>
</template>

<script>
import G6 from '@antv/g6'
import fonts from '@/assets/iconfont.json'
import {
  getTopo
} from '@/api/api'
export default {
  mounted () {
    this.initTopo()
  },
  methods: {
    initTopo () {
      G6.registerNode('iconfont', {
        draw (cfg, group) {
          const { backgroundConfig: backgroundStyle, style, labelCfg: labelStyle } = cfg

          if (backgroundStyle) {
            group.addShape('circle', {
              attrs: {
                x: 0,
                y: 0,
                r: cfg.size,
                ...backgroundStyle
              }
            })
          }

          const keyShape = group.addShape('text', {
            attrs: {
              x: 0,
              y: 0,
              fontFamily: 'iconfont', // 对应css里面的font-family: "iconfont";
              textAlign: 'center',
              textBaseline: 'middle',
              text: cfg.text,
              fontSize: cfg.size,
              ...style
            }
          })
          const labelY = backgroundStyle ? cfg.size * 2 : cfg.size

          group.addShape('text', {
            attrs: {
              x: 0,
              y: labelY,
              textAlign: 'center',
              text: cfg.label,
              ...labelStyle.style
            }
          })
          return keyShape
        }
      })
      const container = document.getElementById('topoTree')
      const width = container.scrollWidth
      const height = container.scrollHeight || 500
      const graph = new G6.Graph({
        container: 'topoTree',
        width,
        height,
        linkCenter: true,
        fitView: true,
        fitViewPadding: [ 50, 50, 100, 50 ],
        modes: {
          default: ['zoom-canvas', 'drag-canvas', 'drag-node', 'activate-relations']
        },
        layout: {
          type: 'gForce',
          preventOverlap: true,
          kr: 10,
          center: [250, 250],
          linkDistance: 100,
          nodeStrength: 30,
          nodeSize: 30
        },
        defaultNode: {
          backgroundConfig: {
            backgroundType: 'circle',
            fill: '#ffffff',
            stroke: '#a6a7ad'
          },
          type: 'iconfont',
          size: 12,
          style: {
            fill: '#0086ff'
          },
          labelCfg: {
            style: {
              fill: '#142132',
              fontSize: 8
            }
          }
        },
        defaultEdge: {
          labelCfg: {
            style: {
              fill: '#142132',
              fontSize: 7
            }
          },
          style: {
            endArrow: {
              path: G6.Arrow.vee(4, 6, 14), // 使用内置箭头路径函数，参数为箭头的 宽度、长度、偏移量（默认为 0，与 d 对应）
              d: 14
            }

          }
        },
        nodeStateStyles: {
          // node style of active state
          active: {
            fillOpacity: 0.8,
            stroke: '#0086ff'
          },
          // node style of selected state
          selected: {
            lineWidth: 5
          }
        },
        edgeStateStyles: {
          // edge style of active state
          active: {
            opacity: 0.5,
            stroke: '#0086ff'
          },
          // edge style of selected state
          selected: {
            stroke: '#0086ff',
            lineWidth: 1
          }
        }
      })
      // graph.setMode('edit')
      getTopo().then((res) => {
        var data = res.data.data
        data.nodes.forEach(node => {
          node.x = Math.random() * 1
          node.text = this.getIcon(node.text)
        })
        // graph.on('afterlayout', e => {
        //   graph.fitView()
        // })
        graph.on('edge:mouseenter', (evt) => {
          const { item } = evt
          graph.setItemState(item, 'active', true)
        })
        graph.on('edge:mouseleave', (evt) => {
          const { item } = evt
          graph.setItemState(item, 'active', false)
        })
        graph.on('edge:click', (evt) => {
          const { item } = evt
          graph.setItemState(item, 'selected', true)
        })
        graph.on('canvas:click', (evt) => {
          graph.getEdges().forEach((edge) => {
            graph.clearItemStates(edge)
          })
        })
        graph.on('node:mouseenter', (evt) => {
          const { item } = evt
          graph.setItemState(item, 'active', true)
        })

        graph.on('node:mouseleave', (evt) => {
          const { item } = evt
          graph.setItemState(item, 'active', false)
        })

        graph.on('node:click', (evt) => {
          const { item } = evt
          graph.setItemState(item, 'selected', true)
        })
        graph.on('canvas:click', (evt) => {
          graph.getNodes().forEach((node) => {
            graph.clearItemStates(node)
          })
        })

        graph.data(data)
        graph.render()
      }).catch((err) => {
        console.log(err)
      })
      if (typeof window !== 'undefined') {
        window.onresize = () => {
          if (!graph || graph.get('destroyed')) return
          if (!container || !container.scrollWidth || !container.scrollHeight) return
          graph.changeSize(container.scrollWidth, container.scrollHeight)
        }
      }
    },
    getIcon (type) {
      const icons = fonts.glyphs.map((icon) => {
        return {
          name: icon.font_class,
          unicode: String.fromCodePoint(icon.unicode_decimal) // `\\u${icon.unicode}`,
        }
      })
      const matchIcon = icons.find((icon) => {
        return icon.name === type
      }) || { unicode: '', name: 'default' }
      return matchIcon.unicode
    }

  },
  data () {
    return {

    }
  }
}
</script>

<style>
  #topoTree {
    background-image: linear-gradient(#eef1f5 1px, transparent 0),linear-gradient(90deg, #eef1f5 1px, transparent 0);
    background-size:10px 10px;
    height: 100%;
  }
</style>

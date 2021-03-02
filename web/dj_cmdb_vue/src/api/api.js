import axios from 'axios'

let host = 'http://127.0.0.1:8888/api'

export const ciSChemaGroup = params => {
  return axios.get(`${host}/ci_schema_group/`, params)
}
export const ciSChema = params => {
  return axios.post(`${host}/ci_schema/`, params)
}
export const CreateSChemaGroup = params => {
  return axios.post(`${host}/ci_schema_group/`, params)
}
export const ciField = params => {
  return axios.get(`${host}/ci_field/`, params)
}
export const createCiField = params => {
  return axios.post(`${host}/ci_field/`, params)
}
export const ciRelation = params => {
  return axios.get(`${host}/relation/`, params)
}
export const createCiRelation = params => {
  return axios.post(`${host}/relation/`, params)
}

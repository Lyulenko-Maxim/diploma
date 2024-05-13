import axios, {type CreateAxiosDefaults} from 'axios'

import {removeFromStorage} from '@/services/auth.service'

const options: CreateAxiosDefaults = {
    baseURL: 'http://localhost:8000/api/',
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true,
}

const axiosClassic = axios.create(options)
const axiosWithAuth = axios.create(options)

axiosWithAuth.interceptors.request.use(config => {
    return config
})

axiosWithAuth.interceptors.response.use(
    config => config,
    async error => {
        if (error?.response?.status === 401) {
            removeFromStorage()
        }
        throw error
    }
)

export {axiosClassic, axiosWithAuth}

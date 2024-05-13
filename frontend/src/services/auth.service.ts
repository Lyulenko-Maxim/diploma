import Cookies from 'js-cookie'
import {cookies} from 'next/headers'
import {IAuthResponse, ILoginForm, IRegisterForm} from '@/types/auth.types'

import {axiosClassic} from '@/api/interceptors'

export enum EnumTokens {
    'ACCESS_TOKEN' = 'access_token',
    'REFRESH_TOKEN' = 'refresh_token'
}

export const authService = {
    async register(data: IRegisterForm) {
        return await axiosClassic.post<IAuthResponse>(
            `/authentication/register/`,
            data
        )
    },

    async activate(token: string) {
        return await axiosClassic.post<IAuthResponse>(
            `/authentication/activate/${token}/`,
        )
    },

    async login(data: ILoginForm) {
        return await axiosClassic.post<IAuthResponse>(
            `/authentication/login/`,
            data
        )
    },

    async logout() {
        const response = await axiosClassic.post('/authentication/logout/')

        if (response.data) removeFromStorage()

        return response
    }
}


// export const getAccessToken = () => {
//     const accessToken = cookies().get(EnumTokens.ACCESS_TOKEN)
//     return accessToken || null
// }

export const removeFromStorage = () => {
    Cookies.remove(EnumTokens.ACCESS_TOKEN)
    Cookies.remove(EnumTokens.REFRESH_TOKEN)
}
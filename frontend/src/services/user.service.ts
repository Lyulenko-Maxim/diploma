import {axiosWithAuth} from '@/api/interceptors'
import {IChangePassword, IProfile, IUser} from "@/types/user.types";


export const userService = {

    async account() {
        const response = await axiosWithAuth.get<IUser>(`/me/account/`,)
        return response.data
    },

    async profile() {
        const response = await axiosWithAuth.get<IProfile>(`/me/profile/`,)
        return response.data
    },

    async editProfile(data: Partial<IProfile>) {
        const response = await axiosWithAuth.patch<IProfile>(`/me/profile/edit/`, data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })

        return response.data
    },

    async changePassword(data: IChangePassword) {
        return await axiosWithAuth.put(`/me/account/change-password/`, data)
    },
}



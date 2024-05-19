import {axiosWithAuth} from '@/api/interceptors'
import {IChangePassword, IProfile, IUser} from "@/types/user.types";


export interface IDeviceRegister {
    name?: string | null,
    registration_id: string,
    device_id?: string | null,
    active: boolean,
    cloud_message_type: "FCM",
    application_id?: null
}

export const notificationService = {

    async registerDevice(data: IDeviceRegister) {
        const response = await axiosWithAuth.post(`/devices/`, data)
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



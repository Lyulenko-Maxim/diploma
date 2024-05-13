import {axiosWithAuth} from "@/api/interceptors";
import {IStatus} from "@/types/status.types";

export const statusService = {

    async list(projectId: string) {
        const response = await axiosWithAuth.get<IStatus[]>(`/dashboard/projects/${projectId}/statuses/`,)
        return response.data
    },

    async retrieve(projectId: string, id: string) {
        const response = await axiosWithAuth.get<IStatus>(`/dashboard/projects/${projectId}/statuses/${id}/`,)
        return response.data
    },

    async create(projectId: string, data: Omit<IStatus, 'id'>) {
        const response = await axiosWithAuth.post<IStatus>(`/dashboard/projects/${projectId}/statuses/`, data)
        return response.data
    },

    async update(projectId: string, id: string, data: Omit<IStatus, 'id'>) {
        const response = await axiosWithAuth.put<IStatus>(`/dashboard/projects/${projectId}/statuses/${id}/`, data)
        return response.data
    },

    async patch(projectId: string, id: string, data: Partial<Omit<IStatus, 'id'>>) {
        const response = await axiosWithAuth.patch<IStatus>(`/dashboard/projects/${projectId}/statuses/${id}/`, data)
        return response.data
    },

    async delete(projectId: string, id: string) {
        const response = await axiosWithAuth.delete(`/dashboard/projects/${projectId}/statuses/${id}/`)
        return response.data
    },

    async move(projectId: string, id: string, data: Pick<IStatus, 'order'>) {
        const response = await axiosWithAuth.patch(`/dashboard/projects/${projectId}/statuses/${id}/move`, data)
        return response.data
    },

}
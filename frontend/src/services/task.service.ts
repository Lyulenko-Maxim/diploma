import {axiosWithAuth} from "@/api/interceptors";
import {ITaskList, ITaskDetail, ITaskInput, ITaskMove} from "@/types/task.types";

export const taskService = {

    async list(projectId: string) {
        const response = await axiosWithAuth.get<ITaskList[]>(`/dashboard/projects/${projectId}/tasks/`,)
        return response.data
    },

    async retrieve(projectId: string, id: string) {
        const response = await axiosWithAuth.get<ITaskDetail>(`/dashboard/projects/${projectId}/tasks/${id}/`,)
        return response.data
    },

    async create(projectId: string, data: ITaskInput) {
        const response = await axiosWithAuth.post(`/dashboard/projects/${projectId}/tasks/`, data)
        return response.data
    },

    async update(projectId: string, id: string, data: ITaskInput) {
        const response = await axiosWithAuth.put(`/dashboard/projects/${projectId}/tasks/${id}/`, data)
        return response.data
    },

    async patch(projectId: string, id: string, data: ITaskInput) {
        const response = await axiosWithAuth.patch(`/dashboard/projects/${projectId}/tasks/${id}/`, data)
        return response.data
    },

    async delete(projectId: string, id: string) {
        const response = await axiosWithAuth.delete(`/dashboard/projects/${projectId}/tasks/${id}/`)
        return response.data
    },

    async move(projectId: string, id: string, data: ITaskMove) {
        const response = await axiosWithAuth.put(`/dashboard/projects/${projectId}/tasks/${id}/move/`, data)
        return response.data
    },

}
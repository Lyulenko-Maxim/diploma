import {axiosWithAuth} from "@/api/interceptors";
import {ITask} from "@/types/task.types";

export const taskService = {

    async list(projectId: string) {
        const response = await axiosWithAuth.get<ITask[]>(`/dashboard/projects/${projectId}/tasks/`,)
        return response.data
    },

    async retrieve(projectId: string, id: string) {
        const response = await axiosWithAuth.get<ITask>(`/dashboard/projects/${projectId}/tasks/${id}/`,)
        return response.data
    },

    async create(projectId: string, data: Partial<Omit<ITask, 'id' | 'key'>>) {
        const response = await axiosWithAuth.post<ITask>(`/dashboard/projects/${projectId}/tasks/`, data)
        return response.data
    },

    async update(projectId: string, id: string, data: Omit<ITask, 'id'>) {
        const response = await axiosWithAuth.put<ITask>(`/dashboard/projects/${projectId}/tasks/${id}/`, data)
        return response.data
    },

    async patch(projectId: string, id: string, data: Partial<Omit<ITask, 'id' | 'key'>>) {
        const response = await axiosWithAuth.patch<ITask>(`/dashboard/projects/${projectId}/tasks/${id}/`, data)
        return response.data
    },

    async delete(projectId: string, id: string) {
        const response = await axiosWithAuth.delete(`/dashboard/projects/${projectId}/tasks/${id}/`)
        return response.data
    },

    async move(projectId: string, id: string, data: Partial<Pick<ITask, 'order' | 'status'>>) {
        const response = await axiosWithAuth.put(`/dashboard/projects/${projectId}/tasks/${id}/move/`, data)
        return response.data
    },

}
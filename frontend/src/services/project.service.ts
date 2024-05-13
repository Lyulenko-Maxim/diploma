import {axiosWithAuth} from "@/api/interceptors";
import {IChangePassword, IProfile, IUser} from "@/types/user.types";
import {IDashboard, IDashboardProject, IProject} from "@/types/project.types";

export const projectService = {
    async dashboard() {
        const response = await axiosWithAuth.get<IDashboard>(`/dashboard/`,)
        return response.data
    },

    async list() {
        const response = await axiosWithAuth.get<IProject[]>(`/dashboard/projects/`,)
        return response.data
    },

    async retrieve(id: string) {
        const response = await axiosWithAuth.get<IProject>(`/dashboard/projects/${id}`,)
        return response.data
    },

    async create(data: Omit<IProject, 'id' | 'slug'>) {
        const response = await axiosWithAuth.post<IProject>(`/dashboard/projects/`, data)
        return response.data
    },

    async update(id: string, data: Omit<IProject, 'id'>) {
        const response = await axiosWithAuth.put<IProject>(`/dashboard/projects/${id}`, data)
        return response.data
    },

    async patch(id: string, data: Partial<Omit<IProject, 'id'>>) {
        const response = await axiosWithAuth.patch<IProject>(`/dashboard/projects/${id}`, data)
        return response.data
    },

    async delete(id: string) {
        const response = await axiosWithAuth.delete(`/dashboard/projects/${id}`,)
        return response.data
    },

    async move(id: string, data: Pick<IDashboardProject, 'order'>) {
        const response = await axiosWithAuth.put(`/dashboard/projects/${id}/move/`, data)
        return response.data
    },

    async invite(id: string, data: Pick<IUser, 'email'>) {
        const response = await axiosWithAuth.post(`/dashboard/projects/${id}/move/`, data)
        return response.data
    },
}
import {axiosWithAuth} from "@/api/interceptors";
import {IMember, IMemberCurrent, IMemberDetails} from "@/types/project.types";

export const memberService = {

    async list(projectId: string) {
        const response = await axiosWithAuth.get<IMember[]>(`/dashboard/projects/${projectId}/members/`,)
        return response.data
    },

    async retrieve(projectId: string, id: string) {
        const response = await axiosWithAuth.get<IMemberDetails>(`/dashboard/projects/${projectId}/members/${id}/`,)
        return response.data
    },

    async current(projectId: string) {
        const response = await axiosWithAuth.get<IMemberCurrent>(`/dashboard/projects/${projectId}/members/current/`,)
        return response.data
    },
}
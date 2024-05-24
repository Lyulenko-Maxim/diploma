import {axiosWithAuth} from "@/api/interceptors";

import {IGroup} from "@/types/group.types";

export const groupService = {

    async list(projectId: string) {
        const response = await axiosWithAuth.get<IGroup[]>(`/dashboard/projects/${projectId}/groups/`,)
        return response.data
    },

    async retrieve(projectId: string, id: string) {
        const response = await axiosWithAuth.get<IGroup>(`/dashboard/projects/${projectId}/groups/${id}/`,)
        return response.data
    },

}
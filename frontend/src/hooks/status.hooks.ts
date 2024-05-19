import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {toast} from "sonner";
import {statusService} from "@/services/status.service";
import {IStatus} from "@/types/status.types";
import {useEffect, useState} from "react";

export const useStatusList = (projectId: string) => {
    const {data} = useQuery({
        queryKey: ['status-list', projectId],
        queryFn: () => statusService.list(projectId),
    })

    const [items, setItems] = useState<IStatus[] | undefined>(data);

    useEffect(() => {
        setItems(data)
    }, [data])

    return {items, setItems}
}

export const useStatusRetrieve = (projectId: string, id: string) => {
    return useQuery({
        queryKey: ['project-retrieve', projectId, id],
        queryFn: () => statusService.retrieve(projectId, id),
    })
}

export const useStatusCreate = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (data: { projectId: string, data: Omit<IStatus, 'id'> }) => {
            return await statusService.create(data.projectId, data.data)
        },

        onSuccess: async (variables, data) => {
            toast.success('Новый статус успешно добавлен')
            await queryClient.invalidateQueries({queryKey: ['status-list', data.projectId,]});
        },

        onError(error) {
            toast.error('Ошибка при создании нового проекта')
            console.error(error)
        }
    })
}

export const useStatusUpdate = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (data: { projectId: string, id: string, data: Omit<IStatus, 'id'> }) => {
            return await statusService.update(data.projectId, data.id, data.data)
        },

        onSuccess: async (variables, data) => {
            toast.success('Статус успешно обновлен')
            await queryClient.invalidateQueries({queryKey: ['status-list', data.projectId,]});
            await queryClient.invalidateQueries({queryKey: ['status-retrieve', data.projectId, data.id]});
        },

        onError(error) {
            toast.error('Ошибка при обновлении статуса')
            console.error(error)
        }
    })
}

export const useStatusPatch = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (data: { projectId: string, id: string, data: Partial<Omit<IStatus, 'id'>> }) => {
            return await statusService.patch(data.projectId, data.id, data.data)
        },

        onSuccess: async (variables, data) => {
            toast.success('Статус успешно обновлен')
            await queryClient.invalidateQueries({queryKey: ['status-list', data.projectId,]});
            await queryClient.invalidateQueries({queryKey: ['status-retrieve', data.projectId, data.id]});
        },

        onError(error) {
            toast.error('Ошибка при обновлении статуса')
            console.error(error)
        }
    })
}

export const useStatusDelete = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (data: { projectId: string, id: string }) => {
            return await statusService.delete(data.projectId, data.id)
        },

        onSuccess: async (variables, data) => {
            toast.success('Статус успешно удален')
            await queryClient.invalidateQueries({queryKey: ['status-list', data.projectId,]});
            await queryClient.invalidateQueries({queryKey: ['status-retrieve', data.projectId, data.id]});
        },

        onError(error) {
            toast.error('Ошибка при удалении статуса')
            console.error(error)
        }
    })
}
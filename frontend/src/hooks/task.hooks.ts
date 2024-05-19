import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {toast} from "sonner";
import {taskService} from "@/services/task.service";
import {ITask} from "@/types/task.types";
import {useEffect, useState} from "react";

export const useTaskList = (projectId: string) => {
    const {data} = useQuery({
        queryKey: ['task-list', projectId],
        queryFn: () => taskService.list(projectId),
    })

    const [items, setItems] = useState<ITask[] | undefined>(data);

    useEffect(() => {
        setItems(data)
    }, [data])

    return {items, setItems}
}

export const useTaskRetrieve = (projectId: string, id: string) => {
    return useQuery({
        queryKey: ['task-retrieve', projectId, id],
        queryFn: () => taskService.retrieve(projectId, id),
    })
}

export const useTaskCreate = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (data: { projectId: string, data: Partial<Omit<ITask, 'id' | 'key'>> }) => {
            return await taskService.create(data.projectId, data.data)
        },

        onSuccess: async (variables, data) => {
            toast.success('Новая задача успешно добавлена')
            await queryClient.invalidateQueries({queryKey: ['task-list', data.projectId,]});
        },

        onError(error) {
            toast.error('Ошибка при добавлении новой задачи')
            console.error(error)
        }
    })
}

export const useTaskUpdate = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (data: { projectId: string, id: string, data: Omit<ITask, 'id'> }) => {
            return await taskService.update(data.projectId, data.id, data.data)
        },

        onSuccess: async (variables, data) => {
            toast.success('Задача успешно обновлена')
            await queryClient.invalidateQueries({queryKey: ['task-list', data.projectId,]});
            await queryClient.invalidateQueries({queryKey: ['task-retrieve', data.projectId, data.id]});
        },

        onError(error) {
            toast.error('Ошибка при обновлении задачи')
            console.error(error)
        }
    })
}

export const useTaskPatch = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (data: { projectId: string, id: string, data: Partial<Omit<ITask, 'id'>> }) => {
            return await taskService.patch(data.projectId, data.id, data.data)
        },

        onSuccess: async (variables, data) => {
            toast.success('Задача успешно обновлена')
            await queryClient.invalidateQueries({queryKey: ['task-list', data.projectId,]});
            await queryClient.invalidateQueries({queryKey: ['task-retrieve', data.projectId, data.id]});
        },

        onError(error) {
            toast.error('Ошибка при обновлении задачи')
            console.error(error)
        }
    })
}

export const useTaskDelete = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (data: { projectId: string, id: string }) => {
            return await taskService.delete(data.projectId, data.id)
        },

        onSuccess: async (variables, data) => {
            toast.success('Задача успешно удалена')
            await queryClient.invalidateQueries({queryKey: ['task-list', data.projectId,]});
            await queryClient.invalidateQueries({queryKey: ['task-retrieve', data.projectId, data.id]});
        },

        onError(error) {
            toast.error('Ошибка при удалении задачи')
            console.error(error)
        }
    })
}

export const useTaskMove = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (data: { projectId: string, id: string, data: Partial<Pick<ITask, 'order' | 'status'>> }) => {
            return await taskService.move(data.projectId, data.id, data.data)
        },

        onSuccess: async (variables, data) => {
            toast.success('Задача успешно перемещена')
            await queryClient.invalidateQueries({queryKey: ['task-list', data.projectId,]});
            await queryClient.invalidateQueries({queryKey: ['task-retrieve', data.projectId, data.id]});
        },

        onError(error) {
            toast.error(error.message)
            console.error(error)
        }
    })
}
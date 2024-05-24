import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {projectService} from "@/services/project.service";
import {IDashboard, IDashboardProject, IProject} from "@/types/project.types";
import {toast} from "sonner";
import {DropResult} from "@hello-pangea/dnd";
import {Dispatch, SetStateAction, useCallback} from "react";

export const useDashboard = () => {
    return useQuery({
        queryKey: ['dashboard'],
        queryFn: () => projectService.dashboard(),
    })
}

export const useProjectRetrieve = (id: string) => {
    return useQuery({
        queryKey: ['project-retrieve', id],
        queryFn: () => projectService.retrieve(id),
    })
}

export const useProjectCreate = () => {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: (data: Omit<IProject, 'id'>) => projectService.create(data),
        onSuccess: async () => {
            toast.success('Проект успешно создан')
            await queryClient.invalidateQueries({queryKey: ['dashboard']});
        },
        onError(error) {
            toast.error('Ошибка при создании нового проекта')
        }
    })
}

// export const usePrepareTableData = (dashboard: IDashboard | undefined) => {
//     return useCallback(() => {
//         if (!dashboard || !dashboard.projects || dashboard.projects.length === 0) {
//             return [];
//         }
//
//         return dashboard.projects.map(({project, order, current_member, random_members, members_count}) => ({
//             id: project.id,
//             name: project.name,
//             owner: project.owner,
//             my_group: current_member.highest_group,
//             members: random_members,
//             members_count: members_count,
//             order: order,
//         }));
//     }, [dashboard]);
// };


export const useProjectDND = (
    projects: IDashboardProject[],
    setProjects: Dispatch<SetStateAction<IDashboardProject[]>>
) => {

    const {mutate, isError} = useProjectMove()
    const onDragEnd = (result: DropResult) => {
        if (!result.destination) return;

        const {source, destination, draggableId} = result;
        console.log(source.index, destination.index);
        if (source.index === destination.index) return;

        const items = Array.from(projects);
        const [movedItem] = items.splice(source.index, 1);
        items.splice(destination.index, 0, movedItem);

        setProjects(items);

        mutate(
            {
                id: draggableId,
                data: {order: destination.index}
            }
        )

        if (isError) setProjects(projects);
    }
    return {onDragEnd}
}


export const useProjectMove = () => {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: (data: {
            id: string,
            data: Pick<IDashboardProject, 'order'>
        }) => projectService.move(data.id, data.data),
        onSuccess: async () => {
            toast.success('Перемещено')
            await queryClient.invalidateQueries({queryKey: ['dashboard']});
        },
    })
}

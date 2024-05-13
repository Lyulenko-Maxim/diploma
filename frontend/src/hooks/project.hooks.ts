import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {projectService} from "@/services/project.service";
import {IDashboard, IDashboardProject, IProject, IProjectTableProps} from "@/types/project.types";
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
        onSuccess() {
            toast.success('Проект успешно создан')
            queryClient.invalidateQueries({queryKey: ['dashboard']});
        },
        onError(error) {
            toast.error('Ошибка при создании нового проекта')
        }
    })
}

export const usePrepareTableData = (dashboard: IDashboard | undefined) => {
    return useCallback((): IProjectTableProps[] => {
        if (!dashboard || !dashboard.projects || dashboard.projects.length === 0) {
            return [];
        }

        return dashboard.projects.map(({project, order, my_group, members, members_count}) => ({
            id: project.id,
            name: project.name,
            slug: project.slug,
            owner: project.owner,
            my_group: my_group,
            members: members,
            members_count: members_count,
            order: order,
        }));
    }, [dashboard]);
};


export const useProjectDND = (
    projects: IProjectTableProps[],
    setProjects: Dispatch<SetStateAction<IProjectTableProps[]>>
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
        onSuccess() {
            toast.success('Перемещено')
            queryClient.invalidateQueries({queryKey: ['dashboard']});
        },
    })
}

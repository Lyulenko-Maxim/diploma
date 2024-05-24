import {useQuery} from "@tanstack/react-query";
import {useEffect, useState} from "react";
import {groupService} from "@/services/group.service";
import {IGroup} from "@/types/group.types";

export const useGroupList = (projectId: string) => {
    const {data} = useQuery({
        queryKey: ['group-list', projectId],
        queryFn: () => groupService.list(projectId),
    })

    const [items, setItems] = useState<IGroup[] | undefined>(data);

    useEffect(() => {
        setItems(data)
    }, [data])

    return {items, setItems}
}

export const useGroupRetrieve = (projectId: string, id: string) => {
    return useQuery({
        queryKey: ['group-retrieve', projectId, id],
        queryFn: () => groupService.retrieve(projectId, id),
        enabled: id !== '',
    })
}

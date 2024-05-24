import {useQuery} from "@tanstack/react-query";
import {useEffect, useState} from "react";
import {memberService} from "@/services/member.service";
import {IMember} from "@/types/project.types";
import {statusService} from "@/services/status.service";

export const useMemberList = (projectId: string) => {
    const {data} = useQuery({
        queryKey: ['member-list', projectId],
        queryFn: () => memberService.list(projectId),
    })

    const [items, setItems] = useState<IMember[] | undefined>(data);

    useEffect(() => {
        setItems(data)
    }, [data])

    return {items, setItems}
}

export const useMemberRetrieve = (projectId: string, id: string) => {
    return useQuery({
        queryKey: ['member-retrieve', projectId, id],
        queryFn: () => memberService.retrieve(projectId, id),
        enabled: id !== '',
    })
}

export const useMemberCurrent = (projectId: string) => {
    return useQuery({
        queryKey: ['member-current', projectId],
        queryFn: () => memberService.current(projectId),
    })
}

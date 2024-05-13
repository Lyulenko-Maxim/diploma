import React, {FC, PropsWithChildren} from 'react';
import {ProjectDetailsProps} from "@/app/me/projects/[id]/page";
import {useStatusList} from "@/hooks/status.hooks";
import StatusItem from "@/components/board/status/StatusItem";

const StatusList: FC<ProjectDetailsProps> = ({params}) => {
    const {data: statuses} = useStatusList(params.id)
    if (!statuses) return <div></div>

    return (
        <div className="flex gap-10 rounded-sm">
            {statuses.map((status, key) => {
                return (
                    <StatusItem key={key} status={status}/>
                )
            })}
        </div>
    );
};

export default StatusList;
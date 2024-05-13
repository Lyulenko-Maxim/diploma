'use client'
import React from 'react';
import {ProjectDetailsProps} from "@/app/me/projects/[id]/page";
import {useProjectRetrieve} from "@/hooks/project.hooks";
import StatusList from "@/components/board/status/StatusList";


const ProjectDetails = ({params}: ProjectDetailsProps) => {
    const {data: project} = useProjectRetrieve(params.id);

    return (
        <div>
            <StatusList params={params}/>
        </div>
    );
};

export default ProjectDetails;
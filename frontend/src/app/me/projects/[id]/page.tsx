import React from 'react';
import ProjectDetails from "@/components/projects/ProjectDetails";

export interface ProjectDetailsProps {
    params: { id: string }
}

const ProjectPage = ({params}: ProjectDetailsProps) => {
    return (
        <ProjectDetails params={params}/>
    );
};

export default ProjectPage;
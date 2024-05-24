"use client";
import React, {FC, useEffect, useState} from 'react';
import {DragDropContext, Droppable} from "@hello-pangea/dnd";
import ProjectItem from "@/components/projects/ProjectItem";
import {useDashboard, useProjectDND} from "@/hooks/project.hooks";
import {CircularProgress, Skeleton} from "@nextui-org/react";
import {IDashboardProject, IProjectListProps} from "@/types/project.types";


const ProjectsList: FC<IProjectListProps> = ({columns}) => {
    const {data: dashboard} = useDashboard();
    const [projects, setProjects] = useState<IDashboardProject[]>([]);
    const {onDragEnd} = useProjectDND(projects, setProjects)

    useEffect(() => {
        if (dashboard?.projects) setProjects(dashboard.projects)

    }, [dashboard])

    if (!dashboard) {
        return (
            <>
                <CircularProgress className='mx-auto flex h-screen justify-center' label={'Loading...'}/>)
            </>
        )
    }

    return (
        <DragDropContext onDragEnd={onDragEnd}>
            <Droppable droppableId="projects">
                {(provided) => (
                    <div {...provided.droppableProps}
                         ref={provided.innerRef}>

                        {projects.map((item) => (
                            <ProjectItem key={item.id} item={item} index={item.order} columns={columns}/>
                        ))}

                        {provided.placeholder}
                    </div>
                )}
            </Droppable>
        </DragDropContext>
    );
};

export default ProjectsList;
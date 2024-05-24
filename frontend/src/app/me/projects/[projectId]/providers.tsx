'use client'
import {createContext, ReactNode, useContext, useEffect} from 'react';
import {useProjectRetrieve} from "@/hooks/project.hooks";
import {addRecentProject} from "@/app/me/projects/recent";

const ProjectParamsContext = createContext('');

export const useProjectParams = () => useContext(ProjectParamsContext);

export const ProjectParamsProvider = ({projectId, children}: {
    projectId: string,
    children: ReactNode
}) => {

    const {data: project} = useProjectRetrieve(projectId);
    useEffect(() => {
        if (project) addRecentProject(project);
    }, [project]);

    return (
        <ProjectParamsContext.Provider value={projectId}>
            {children}
        </ProjectParamsContext.Provider>
    );
};
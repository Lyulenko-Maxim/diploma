import {IProject} from "@/types/project.types";

const RECENT_PROJECTS_KEY = 'recentProjects';
const MAX_RECENT_PROJECTS = 3;

export interface IResentProject extends IProject {
    lastVisited: string;
}

const getRecentProjects = (): IResentProject[] => {
    const storedProjects = localStorage.getItem(RECENT_PROJECTS_KEY);
    return storedProjects ? JSON.parse(storedProjects) : [];
};

const addRecentProject = (project: IProject) => {
    const recentProjects = getRecentProjects();
    const currentTime = new Date().toISOString();

    const updatedProject: IResentProject = {...project, lastVisited: currentTime};

    const updatedProjects = [updatedProject, ...recentProjects.filter(p => p.id !== project.id)].slice(0, MAX_RECENT_PROJECTS);
    localStorage.setItem(RECENT_PROJECTS_KEY, JSON.stringify(updatedProjects));
};

export {getRecentProjects, addRecentProject};
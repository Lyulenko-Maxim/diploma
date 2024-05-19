import {IBase} from "@/types/root.types";
import {IStatus} from "@/types/status.types";
import {IMarker} from "@/types/marker.types";
import {IProject, IProjectMember} from "@/types/project.types";
import {IComment} from "@/types/comment.types";

export enum PriorityEnum {
    CRITICAL = 'critical',
    HIGHEST = 'highest',
    HIGH = 'high',
    MEDIUM = 'medium',
    LOW = 'low',
    LOWEST = 'lowest',
}

export interface ITask extends IBase {
    key: string,
    status: string,
    title: string,
    description: string | null,
    priority: PriorityEnum | PriorityEnum.MEDIUM,
    markers: IMarker[] | [],
    due_date: Date | null,
    is_archived: boolean,
    project: IProject,
    author: IProjectMember,
    assignee: IProjectMember | null,
    parent: ITask | null,
    dependencies: ITask[] | [],
    available_dependencies: ITask[] | [],
    comments: IComment[] | [],
    order: number | 0
}
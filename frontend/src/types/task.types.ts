import {IBase} from "@/types/root.types";
import {IStatus} from "@/types/status.types";
import {IMarker} from "@/types/marker.types";
import {IMember, IProject} from "@/types/project.types";
import {IComment} from "@/types/comment.types";

export enum PriorityEnum {
    CRITICAL = 'critical',
    HIGHEST = 'highest',
    HIGH = 'high',
    MEDIUM = 'medium',
    LOW = 'low',
    LOWEST = 'lowest',
}

export interface ITaskList extends IBase {
    title: string,
    start_date?: Date,
    end_date?: Date,
    duration?: number,
    priority: PriorityEnum,
    status: IStatus,
    author: IMember,
    assignee?: IMember,
    markers: IMarker[],
    order: number
}

export interface ITaskDetail extends ITaskList {
    description?: string,
    dependencies: ITaskList[],
    available_dependencies: ITaskList[],
    comments: IComment[],
}

export interface ITaskInput extends Partial<Omit<ITaskDetail, 'id' | 'title' | 'status'>> {
    title: string;
    status: string,
}

export interface ITaskMove {
    status: string,
    order: number
}

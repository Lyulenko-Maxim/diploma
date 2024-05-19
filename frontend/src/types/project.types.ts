import {IBase} from "@/types/root.types";
import {IProfile, IProfilePublic} from "@/types/user.types";
import {IGroup} from "@/types/group.types";


export interface IProject extends IBase {
    name: string,
    description: string,
    owner: IProfilePublic,
}

export interface IProjectInput extends Omit<IProject, 'id' | 'owner'> {
}

export interface IDashboard extends IBase {
    owner: string,
    projects: IDashboardProject[]
}

export interface IMember extends IBase {
    profile: IProfilePublic
    highest_group: IGroup
}

export interface IMemberDetails extends IMember {
    groups: IGroup[]
}

export interface IDashboardProject extends IBase {
    project: IProject
    owner: IMember
    dashboard: Pick<IDashboard, 'id'>
    order: number
    current_member: IMember
    random_members: IMember[]
    members_count: number
}


export interface IProjectColumn {
    key: string,
    label: string,
}

export interface IProjectListProps {
    columns: IProjectColumn[]
}

export interface IProjectItemProps {
    item: IDashboardProject,
    index: number,
    columns: IProjectColumn[]
}
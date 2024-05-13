import {IBase} from "@/types/root.types";
import {IProfile} from "@/types/user.types";
import {IGroup} from "@/types/group.types";


export interface IProject extends IBase {
    name: string,
    slug: string,
    description: string,
    owner: IProfile,
}

export interface IDashboard extends IBase {
    owner: Pick<IProfile, 'id'>,
    projects: IDashboardProject[]
}

export interface IProjectMember extends IBase {
    profile: IProfile
    date_joined: Date,
    deactivated: boolean,
    groups: IGroup
}

export interface IDashboardProject extends IBase {
    project: Omit<IProject, 'description'>
    dashboard: Pick<IDashboard, 'id'>
    order: number
    my_group: IGroup
    members: IProjectMember[]
    members_count: number
}

export interface IProjectTableProps {
    id: string,
    name: string,
    slug: string,
    owner: IProfile,
    my_group: IGroup,
    members: IProjectMember[],
    members_count: number,
    order: number,
}

export interface IProjectColumn {
    key: string,
    label: string,
}

export interface IProjectListProps {
    columns: IProjectColumn[]
}

export interface IProjectItemProps {
    item: IProjectTableProps,
    index: number,
    columns: IProjectColumn[]
}
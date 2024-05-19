import {IBase} from "@/types/root.types";
import {IProjectMember} from "@/types/project.types";

export interface IComment extends IBase {
    content: string,
    owner: IProjectMember,
    created_at: Date,
    last_edit: Date,
}
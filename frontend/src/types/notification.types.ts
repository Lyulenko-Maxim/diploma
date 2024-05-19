import {IBase} from "@/types/root.types";
import {IProject} from "@/types/project.types";
import {IProfilePublic} from "@/types/user.types";

export interface IInvitation extends IBase {
    project: IProject,
    sender: IProfilePublic,
}
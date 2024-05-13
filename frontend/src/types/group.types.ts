import {IBase} from "@/types/root.types";
import {IProfile} from "@/types/user.types";

export interface IPermission extends IBase {
    name: string,
    code: string,
}

export interface IGroup extends IBase {
    name: string,
    color_hex: string,
    order: number,
    permissions: IPermission[]
}
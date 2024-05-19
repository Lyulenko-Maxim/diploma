import {IBase} from "@/types/root.types";

export enum StatusCategoryEnum {
    TODO = 'todo',
    DEFAULT = 'default',
    COMPLETED = 'completed',
}

export interface IStatus extends IBase {
    name: string,
    category: StatusCategoryEnum | StatusCategoryEnum.DEFAULT,
    order: number,
}
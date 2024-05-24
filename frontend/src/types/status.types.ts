import {IBase} from "@/types/root.types";

export enum StatusCategoryEnum {
    TODO = 'todo',
    DEFAULT = 'default',
    COMPLETED = 'completed',
}

export interface IStatus extends IBase {
    name: string,
    category: StatusCategoryEnum,
    order: number,
}

export interface IStatusInput extends Omit<IStatus, 'id'> {

}

export interface IStatusMove extends Pick<IStatus, 'order'> {

}
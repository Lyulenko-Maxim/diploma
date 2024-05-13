import {IBase} from "@/types/root.types";

export interface IStatus extends IBase {
    name: string,
    category: 'todo' | 'default' | 'completed',
    order: number,
}
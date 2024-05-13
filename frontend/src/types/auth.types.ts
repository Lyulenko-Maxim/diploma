import {IUser} from "@/types/user.types";

export interface ILoginForm {
    email: string
    password: string
}

export interface IRegisterForm {
    email: string
    password: string
    repeat_password: string
}

export interface IAuthResponse {
    user: IUser
}

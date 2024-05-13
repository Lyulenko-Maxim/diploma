export interface IUser {
    id: string
    email: string,
}


export interface IProfile {
    id: string,
    username: string,
    first_name?: string,
    last_name?: string,
    online?: boolean,
    photo?: string | File,
    banner_color_hex?: string,
}

export interface IChangePassword {
    old_password: string,
    new_password: string,
    new_password_repeat: string,
}
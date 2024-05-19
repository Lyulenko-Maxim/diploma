export interface IUser {
    id: string
    email: string,
    deleted_at: Date,
}


export interface IChangePassword {
    old_password: string,
    new_password: string,
    new_password_repeat: string,
}

export interface IProfile {
    id: string,
    user: IUser,
    username: string,
    first_name: string,
    last_name: string,
    photo: string,
    banner_color_hex: string,
}

export interface IProfilePublic extends Omit<IProfile, 'user'> {
}

export interface IProfileInput extends Omit<IProfile, 'id' | 'photo'> {
    photo: File
}

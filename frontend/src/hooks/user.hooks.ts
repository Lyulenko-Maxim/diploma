import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import {userService} from "@/services/user.service";
import {useEffect, useState} from "react";
import {IChangePassword, IProfile, IUser} from "@/types/user.types";
import {toast} from "sonner";
import {useForm} from "react-hook-form";

export const useUser = () => {
    const {data} = useQuery({
        queryKey: ['account'],
        queryFn: () => userService.account(),
    })

    const [user, setUser] = useState<IUser | undefined>(data)

    useEffect(() => {
        setUser(data)
    }, [data])

    return {user, setUser}
}

export const useProfile = () => {
    return useQuery({
        queryKey: ['profile'],
        queryFn: () => userService.profile(),
    })
}

export const useEditProfile = () => {
    const queryClient = useQueryClient()
    const {mutate, isPending, isSuccess, isError} = useMutation({
        mutationKey: ['profile-edit'],
        mutationFn: (data: Partial<IProfile>) => userService.editProfile(data),
        gcTime: 0,
        onSuccess() {
            toast.success('Профиль успешно обновлен')
            queryClient.invalidateQueries({queryKey: ['profile']});
        },
        onError(error) {
            toast.error('Ошибка')
        }

    })

    return {mutate, isPending,}
}

export const useChangePassword = () => {
    const {register, handleSubmit, reset} = useForm<IChangePassword>({mode: 'onChange'})
    const {mutate, isPending, isSuccess, isError} = useMutation({
        mutationKey: ['change-password'],
        mutationFn: (data: IChangePassword) => userService.changePassword(data),
        gcTime: 0,
        onSuccess() {
            toast.success('Пароль успешно изменен')
            reset()
        },
        onError(error) {
            toast.error('Ошибка')
        }

    })
    return {mutate, isPending, register, handleSubmit, reset}
}


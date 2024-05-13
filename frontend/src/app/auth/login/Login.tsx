'use client'

import {useMutation} from '@tanstack/react-query'
import {useRouter} from 'next/navigation'
import {useState} from 'react'
import {SubmitHandler, useForm} from 'react-hook-form'
import {authService} from '@/services/auth.service'
import {ILoginForm} from "@/types/auth.types";
import {Input} from '@nextui-org/input'
import {EyeSlashFilledIcon, EyeIcon, MailIcon} from "@nextui-org/shared-icons";
import {toast} from "sonner";
import AuthForm from "@/app/auth/AuthForm";

export function Login() {
    const {register, handleSubmit, reset} = useForm<ILoginForm>({
        mode: 'onChange'
    })
    const [isVisible, setIsVisible] = useState(false);

    const {replace} = useRouter()
    const [error, setError] = useState<Error | null>(null);

    const {mutate, isPending} = useMutation({
        mutationKey: ['login'],
        mutationFn: (data: ILoginForm) => authService.login(data),
        gcTime: 0,
        onSuccess() {
            toast.success('Успешный вход')
            replace('/me')
        },
        onError(error) {
            toast.error('Ошибка')
            setError(error)
        }
    })

    const onSubmit: SubmitHandler<ILoginForm> = data => mutate(data)
    const toggleVisibility = () => setIsVisible(!isVisible);

    return (
        <AuthForm type='login' onSubmit={handleSubmit(onSubmit)} isPending={isPending}>
            <Input label="Email"
                   placeholder="Введите Email"
                   type="email"
                   variant="underlined"
                   endContent={
                       <MailIcon className="text-2xl text-default-400 pointer-events-none flex-shrink-0"/>
                   }
                   {...register('email', {
                       required: 'Email обязательный!'
                   })}
                   className="max-w-xs mx-auto"
            />
            <Input label="Пароль"
                   placeholder="Введите пароль"
                   variant="underlined"
                   type={isVisible ? "text" : "password"}
                   endContent={
                       <button className="focus:outline-none" type="button" onClick={toggleVisibility}>
                           {isVisible
                               ? <EyeIcon className="text-2xl text-default-400 pointer-events-none"/>
                               : <EyeSlashFilledIcon
                                   className="text-2xl text-default-400 pointer-events-none"/>
                           }
                       </button>
                   }
                   className="max-w-xs mx-auto"
                   {...register('password', {
                       required: 'Пароль обязательный!'
                   })}
            />
        </AuthForm>
    )
}
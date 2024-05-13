'use client'

import {useMutation} from '@tanstack/react-query'
import {useRouter, useSearchParams} from 'next/navigation'
import {useState} from 'react'
import {SubmitHandler, useForm} from 'react-hook-form'
import {authService} from '@/services/auth.service'
import {IRegisterForm} from "@/types/auth.types";
import {Input} from '@nextui-org/input'
import {EyeFilledIcon, EyeIcon, EyeSlashFilledIcon, MailIcon} from "@nextui-org/shared-icons";
import {toast} from "sonner";
import AuthForm from "@/app/auth/AuthForm";
import {bool} from "prop-types";

const Register = () => {
    const {register, handleSubmit, reset, formState: {errors}} = useForm<IRegisterForm>({
        mode: 'onChange'
    })
    const [isVisible, setIsVisible] = useState(false);

    const {replace, push} = useRouter()
    const [error, setError] = useState<Error | null>(null);


    const {mutate, isPending} = useMutation({
        mutationKey: ['register'],
        mutationFn: (data: IRegisterForm) => authService.register(data),
        gcTime: 0,
        onSuccess() {
            push('register/verification')
            toast.info('Требуется подтверждение по электронной почте')
        },
        onError(error) {
            toast.error('Ошибка')
            setError(error)
        }
    })

    const onSubmit: SubmitHandler<IRegisterForm> = data => mutate(data)
    const toggleVisibility = () => setIsVisible(!isVisible);

    return (
        <AuthForm type='register' onSubmit={handleSubmit(onSubmit)} isPending={isPending}>
            <Input label="Email"
                   placeholder="Введите email"
                   type="email"
                   variant="underlined"
                   endContent={
                       <MailIcon className="text-2xl text-default-400 pointer-events-none flex-shrink-0"/>
                   }
                   {...register('email', {
                       required: 'Email обязательный!'
                   })}
                   className="max-w-xs mx-auto"
                   isInvalid={!!errors.email}
                   errorMessage={errors.email?.message}
            />

            <Input label="Пароль"
                   placeholder="Введите пароль"
                   variant="underlined"
                   type={isVisible ? "text" : "password"}
                   endContent={
                       <button className="focus:outline-none" type="button"
                               onMouseDown={toggleVisibility}
                               onMouseUp={toggleVisibility}>
                           {isVisible
                               ? <EyeSlashFilledIcon className="text-2xl text-default-400 pointer-events-none"/>
                               : <EyeIcon className="text-2xl text-default-400 pointer-events-none"/>
                           }
                       </button>
                   }
                   className="max-w-xs mx-auto"
                   {...register('password', {
                       required: 'Пароль обязательный!'
                   })}
            />
            <Input label="Повторите пароль"
                   placeholder="Повторите пароль"
                   variant="underlined"
                   type={isVisible ? "text" : "password"}
                   endContent={
                       <button className="focus:outline-none" type="button" onClick={toggleVisibility}>
                           {isVisible
                               ? <EyeSlashFilledIcon className="text-2xl text-default-400 pointer-events-none"/>
                               : <EyeIcon className="text-2xl text-default-400 pointer-events-none"/>
                           }
                       </button>
                   }
                   className="max-w-xs mx-auto"
                   {...register('repeat_password', {
                       required: 'Пароль обязательный!'
                   })}
            />


        </AuthForm>
    )
};

export default Register;


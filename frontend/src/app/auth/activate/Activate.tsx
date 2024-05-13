'use client'

import {useMutation} from '@tanstack/react-query'
import {useRouter, useSearchParams} from 'next/navigation'
import {useEffect, useState} from 'react'
import {notFound} from 'next/navigation'

import {authService} from '@/services/auth.service'
import {Spinner} from "@nextui-org/spinner";
import {toast} from "sonner";

export function Activate() {
    const {replace} = useRouter()
    const [error, setError] = useState<Error | null>(null);
    const searchParams = useSearchParams()
    const token = searchParams.get('token')

    const {mutate} = useMutation({
        mutationKey: ['activate'],
        mutationFn: (token: string) => authService.activate(token),
        gcTime: 0,
        onSuccess() {
            replace('/auth/login')
            toast.success('Успешная активация аккаунта!\nВойдите в аккаунт используя свои учетные данные.')
        },
        onError(error) {
            setError(error)
        }
    })

    useEffect(() => {
        if (!token) notFound();

        mutate(token);

        if (error) notFound();

    }, [error, mutate, token]);

    return (
        <Spinner label="Активация аккаунта..." color="success" labelColor="success"/>
    )
}
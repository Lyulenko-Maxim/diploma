import React, {FC, PropsWithChildren} from 'react';
import Link from "next/link";
import {Button} from "@nextui-org/button";
import Image from "next/image";
import {GanttChart} from "lucide-react";

interface AuthFormProps {
    type: 'login' | 'register'
    onSubmit: () => void;
    isPending: boolean,
}

const AuthForm: FC<PropsWithChildren & AuthFormProps> = (
    {
        type,
        onSubmit,
        isPending,
        children,

    }
) => {
    return (
        <div className='flex min-h-screen'>
            <form
                className='w-1/4 m-auto shadow bg-sidebar rounded-xl p-layout py-10'
                onSubmit={onSubmit}>
                <div className='w-fit flex flex-col gap-5 items-center mx-auto'>
                    <div className='flex items-center'>
                        <span className={'flex items-center font-medium text-2xl'}>SYN<GanttChart size={32}
                                                                                                  className="fill-foreground"/>RGY</span>
                        {/*<h1 className='font-light text-gray-500'>SYNERGY</h1>*/}
                    </div>
                    <h3 className="text-2xl font-medium text-default-900">
                        {type === 'login'
                            ? 'Войдите в свой аккаунт'
                            : 'Создайте аккаунт'
                        }
                    </h3>

                    {type === 'login'
                        ? <span className='text-sm font-normal'>Еще нет аккаутна?
                                <Link href={'./register'} className='text-primary'> Создать</Link></span>
                        : <span className='text-sm font-normal'>Уже есть аккаунт?
                                <Link href={'./login'} className='text-primary'> Войти</Link></span>
                    }

                    {children}

                    {/*{type === 'login' ?*/}
                    {/*    <div className='w-full flex flex-col items-end'>*/}
                    {/*        <Link href={'/'} className='text-sm font-normal text-primary'>*/}
                    {/*            Забыли пароль?*/}
                    {/*        </Link>*/}
                    {/*    </div> : ''*/}
                    {/*}*/}

                    <Button
                        radius={"sm"}
                        type={"submit"}
                        color="primary"
                        variant="shadow"
                        isDisabled={isPending}
                        isLoading={isPending}
                        className='max-w-xs mx-auto w-full'>
                        {type === 'login' ? 'Войти' : 'Создать'}
                    </Button>
                </div>
            </form>
        </div>
    );
};

export default AuthForm;
import React, {useEffect, useRef} from 'react';
import {Input, CircularProgress} from "@nextui-org/react";
import {Button} from "@nextui-org/button";
import {useEditProfile, useProfile} from "@/hooks/user.hooks";
import {SubmitHandler, useForm} from "react-hook-form";
import {IProfile} from "@/types/user.types";

const Profile = () => {
    const {data: profile, isPending: isProfilePending} = useProfile()
    const {register, handleSubmit, reset} = useForm<IProfile>(
        {
            mode: 'onChange',
            defaultValues: {
                username: profile?.username,
                first_name: profile?.first_name,
                last_name: profile?.last_name,
            }
        }
    )

    const {mutate, isPending} = useEditProfile()

    const onSubmit: SubmitHandler<IProfile> = data => {
        mutate(data)
    }
    if (!profile) {
        return <CircularProgress/>
    }
    return (
        <>
            <h1 className='px-1'>Редактирование профиля</h1>
            <form onSubmit={handleSubmit(onSubmit)}>
                <div className='mx-auto flex w-fit flex-col items-center gap-5'>
                    <Input label="Отображаемое имя"
                           placeholder={"Введите отображаемое имя"}
                           variant="underlined"
                           type='text'
                           className="mx-auto max-w-xs"
                           defaultValue={profile.username}
                           {...register('username')}
                    />
                    <Input label="Имя"
                           placeholder={"Введите ваше имя"}
                           variant="underlined"
                           type='text'
                           className="mx-auto max-w-xs"
                           defaultValue={profile.first_name}
                           {...register('first_name')}
                    />
                    <Input label="Фамилия"
                           placeholder={"Введите вашу фамилию"}
                           variant="underlined"
                           type='text'
                           className="mx-auto max-w-xs"
                           defaultValue={profile.last_name}
                           {...register('last_name')}
                    />
                    <Button
                        radius={"sm"}
                        type={"submit"}
                        color="primary"
                        variant="shadow"
                        isDisabled={isPending}
                        isLoading={isPending}
                        className='mx-auto w-full max-w-xs'>
                        Сохранить
                    </Button>
                </div>
            </form>
        </>
    );
};

export default Profile;
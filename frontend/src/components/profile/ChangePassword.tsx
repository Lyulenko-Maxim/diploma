import React, {useState} from 'react';
import {Input} from "@nextui-org/react";
import {Button} from "@nextui-org/button";
import {EyeIcon, EyeSlashFilledIcon} from "@nextui-org/shared-icons";
import {SubmitHandler} from "react-hook-form";
import {useChangePassword} from "@/hooks/user.hooks";
import {IChangePassword} from "@/types/user.types";

const ChangePassword = () => {
    const [isVisible, setIsVisible] = useState(false);
    const {mutate, isPending, register, handleSubmit} = useChangePassword()
    const onSubmit: SubmitHandler<IChangePassword> = data => mutate(data)
    const toggleVisibility = () => setIsVisible(!isVisible);

    return (
        <>
            <h1 className='px-1'>Сменить пароль</h1>
            <form onSubmit={handleSubmit(onSubmit)}>
                <div className='w-fit flex flex-col gap-5 items-center mx-auto'>
                    <Input label="Текущий пароль"
                           placeholder="Введите текущий пароль"
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
                           {...register('old_password', {required: 'Пароль обязательный!'})}
                    />
                    <Input label="Новый пароль"
                           placeholder="Введите новый пароль"
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
                           {...register('new_password', {
                               required: 'Пароль обязательный!'
                           })}
                    />
                    <Input label="Повтор нового пароля"
                           placeholder="Повторите новый пароль"
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
                           {...register('new_password_repeat', {
                               required: 'Пароль обязательный!'
                           })}
                    />
                    <Button
                        radius={"sm"}
                        type={"submit"}
                        color="primary"
                        variant="shadow"
                        isDisabled={isPending}
                        isLoading={isPending}
                        className='max-w-xs mx-auto w-full'>
                        Сменить
                    </Button>
                </div>
            </form>
        </>
    );
};

export default ChangePassword;
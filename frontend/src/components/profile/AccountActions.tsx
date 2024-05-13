import React from 'react';
import {Button} from "@nextui-org/button";
import {Delete, PowerOff, Trash} from "lucide-react";

const AccountActions = () => {
    return (
        <>
            <h1>Удаление учетной записи</h1>
            <p className='font-light'>
                Отключив учетную запись, вы в любой момент сможете восстановить её.<br/>
                После нажатия кнопки уведомления, ваша учетная запись будет деактивирована.<br/>
                В течении <span className='font-normal'>14 дней</span> после запроса на удаление, вы моежете
                восстановить вашу учетную запись.<br/>
                По истечении этого срока восстановить учетную запись будет <span
                className='font-normal'>невозможно!</span>
            </p>
            <div className="flex items-center gap-4">
                <Button
                    radius={"sm"}
                    type='button'
                    color="warning"
                    variant="ghost"
                    className='max-w-xs  w-full'
                    startContent={<PowerOff size={20}/>}>
                    Отключить учетную запись
                </Button>
                <Button
                    radius={"sm"}
                    type='button'
                    color="danger"
                    variant="ghost"
                    className='max-w-xs w-full'
                    startContent={<Trash size={20}/>}>
                    Удалить учетную запись
                </Button>
            </div>
        </>
    );
};

export default AccountActions;
'use client'
import React, {ChangeEvent, ChangeEventHandler, LegacyRef, useEffect, useRef, useState} from 'react';
import {useEditProfile, useProfile, useUser} from "@/hooks/user.hooks";
import {
    Avatar,
    Button,
    Card,
    CardBody,
    Input,
    Image,
    Popover,
    PopoverContent,
    PopoverTrigger,
    Tab,
    Tabs, CircularProgress
} from "@nextui-org/react";
import {Camera, Edit, Mail, Pipette} from "lucide-react";
import {Divider} from "@nextui-org/divider";
import ChangePassword from "@/components/profile/ChangePassword";
import AccountActions from "@/components/profile/AccountActions";
import Profile from "@/components/profile/Profile";
import clsx from "clsx";
import {BlockPicker, ChromePicker, Color, ColorPickerProps, ColorResult, SketchPicker, SliderPicker} from "react-color";
import {Header} from "next/dist/lib/load-custom-routes";
import NextImage from "next/image";

const Account = () => {

    const {user} = useUser()
    let tabs = [
        {
            id: "photos",
            label: "Профиль",
            content: <Profile/>
        },
        // {
        //     id: "email",
        //     label: "Email",
        //     content: "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        // },
        {
            id: "pass",
            label: "Пароль",
            content: <ChangePassword/>
        },
        // {
        //     id: "conf",
        //     label: "Конфиденциальность",
        //     content: "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        // },
        {
            id: "account",
            label: "Аккаунт",
            content: <AccountActions/>
        }
    ];

    const {mutate} = useEditProfile()
    const {data: profile, isPending} = useProfile()

    const [colorPickerState, setColorPickerState] = useState({
        isVisible: false,
        color: profile?.banner_color_hex,
    })

    const handleOnChangeComplete = (color: ColorResult) => {
        setColorPickerState({...colorPickerState, color: color.hex});
        mutate(({banner_color_hex: color.hex}));
    };

    const handleChange = (color: any) => {
        setColorPickerState({...colorPickerState, color: color.hex});
    };
    const [selectedImage, setSelectedImage] = useState<File | null>(null);
    const headerRef = useRef<HTMLElement>(null)
    const avatarRef = useRef<HTMLInputElement>(null)
    const handleAvatarClick = () => {
        if (avatarRef.current) {
            avatarRef.current.click();
        }
    };
    const handleImageChange = (event: ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files
        if (files) {
            const file = files[0];
            setSelectedImage(file);
            mutate({photo: file})
        }
    };

    useEffect(() => {
        if (headerRef.current && profile?.banner_color_hex) {
            headerRef.current.style.backgroundColor = profile.banner_color_hex
        }
    }, [headerRef, colorPickerState.color, profile])

    if (!profile) {
        return <CircularProgress color='primary' label="Loading..."
                                 className={'flex w-full h-full m-auto justify-center'}/>
    }

    return (
        <div className='m-8 rounded-xl shadow-xl bg-sidebar'>
            <header ref={headerRef}
                    className='h-32 overflow-hidden rounded-t-xl shadow hover:cursor-pointer'>
                <div
                    className='h-full w-full bg-black bg-opacity-0 transition duration-300 ease-in-out group hover:bg-opacity-30'>
                    <Popover showArrow placement="bottom" shouldBlockScroll>
                        <PopoverTrigger>
                            <div className='flex h-full w-full items-center justify-center'>
                                <Button isDisabled variant='light'
                                        className='text-white opacity-0 transition duration-300 ease-in-out group-hover:opacity-100'
                                        startContent={<Pipette strokeWidth={2}/>}>
                                    Сменить цвет фона
                                </Button>
                            </div>
                        </PopoverTrigger>
                        <PopoverContent className="mt-1 p-0">
                            <BlockPicker
                                color={profile?.banner_color_hex}
                                onChange={handleChange}
                                onChangeComplete={handleOnChangeComplete}
                            />
                        </PopoverContent>
                    </Popover>
                </div>
            </header>
            <div className='flex flex-col gap-4 px-10'>
                <div className='relative mt-8 flex items-center gap-10'>
                    <div onClick={handleAvatarClick} className='relative group'>
                        <input type={'file'}
                               accept="image/*"
                               ref={avatarRef}
                               onChange={handleImageChange}
                               className={'hidden'}
                        />
                        {profile.photo
                            ? <Image
                                as={NextImage}
                                width={200}
                                height={200}
                                radius='full'
                                src={typeof (profile?.photo) == 'string' ? profile?.photo : '/'}
                                className="h-24 w-24 object-cover text-xl transition ease-in-out hover:cursor-pointer"
                                alt="Avatar"
                            />
                            :<div className="flex h-24 w-24 items-center justify-center rounded-full border-2 object-cover text-xl transition ease-in-out border-foreground/50 hover:cursor-pointer">
                                <Camera strokeWidth={2} size={24} />
                            </div>

                        }
                        <div
                            className={
                                'absolute top-0 right-0 bottom-0 left-0 z-10 flex h-full w-full items-center justify-center ' +
                                'rounded-full bg-black bg-opacity-0 opacity-0 transition duration-300 ease-in-out ' +
                                'group-hover:bg-opacity-30 group-hover:opacity-100 group-hover:cursor-pointer'
                            }>
                            <Edit className='text-white'/>
                        </div>
                    </div>

                    {/*<Avatar showFallback*/}
                    {/*        className="h-24 w-24 text-xl hover:cursor-pointer"*/}
                    {/*        fallback={*/}
                    {/*            <Camera className="text-default-500 hover:animate-pulse" fill="currentColor" size={24}/>*/}
                    {/*        }*/}
                    {/*        onClick={handleAvatarClick}*/}
                    {/*/>*/}

                    <div className="max-w-md">
                        <div className="space-y-1">
                            <h4 className="font-medium text-large">{profile?.username}</h4>
                            {/*<p className="text-small text-default-400">short-description.</p>*/}
                        </div>
                        <Divider className="my-4"/>
                        <div className="flex h-5 items-center space-x-4 text-small">
                            <div className='flex items-center gap-1'><Mail size={20}/> {user?.email}</div>
                            <Divider orientation="vertical"/>
                            {/*<div>Docs</div>*/}
                            {/*<Divider orientation="vertical"/>*/}
                            {/*<div>Source</div>*/}
                        </div>
                    </div>

                </div>
                <Divider className="my-4"/>
                <div className="flex w-full flex-col">
                    <Tabs aria-label="Dynamic tabs" items={tabs}>
                        {(item) => (
                            <Tab key={item.id} title={item.label}>
                                <div className='my-4 flex w-fit flex-col gap-5 bg-sidebar'>
                                    {item.content}
                                </div>
                            </Tab>
                        )}
                    </Tabs>
                </div>
            </div>
        </div>

    )
        ;
};

export default Account;
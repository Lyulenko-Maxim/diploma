'use client'
import React, {ReactNode} from 'react';
import {Navbar, NavbarBrand, NavbarContent, NavbarItem} from "@nextui-org/react";
import {BurguerButton} from "@/components/navbar/burguer-button";
import Link from "next/link";
import Image from "next/image";
import {NotificationsDropdown} from "@/components/navbar/notifications-dropdown";
import {CircleHelp, GanttChart, Kanban, Puzzle} from "lucide-react";
import {UserDropdown} from "@/components/navbar/user-dropdown";
import clsx from "clsx";
import {usePathname} from "next/navigation";

export default function MainLayout({children,}: {
    children: ReactNode
}) {
    const pathname = usePathname();

    return (
        <div className="relative flex flex-col flex-1 overflow-y-hidden overflow-x-hidden h-screen">
            <Navbar
                isBordered
                className="w-full"
                classNames={{
                    wrapper: "w-full max-w-full",
                    item: [
                        "flex",
                        "relative",
                        "h-full",
                        "items-center",
                        "data-[active=true]:text-primary",
                        "data-[active=true]:after:content-['']",
                        "data-[active=true]:after:absolute",
                        "data-[active=true]:after:bottom-0",
                        "data-[active=true]:after:left-0",
                        "data-[active=true]:after:right-0",
                        "data-[active=true]:after:h-[2px]",
                        "data-[active=true]:after:rounded-[2px]",
                        "data-[active=true]:after:bg-primary",
                    ],
                }}
            >
                <NavbarContent className="md:hidden">
                    <BurguerButton/>
                </NavbarContent>

                <NavbarBrand className='flex-grow-0 mr-4 basis-auto'>
                    <Link href={'/me'} className={'flex gap-1 justify-center items-center font-light'}>
                        <span className={'flex items-center font-medium text-2xl'}>SYN<GanttChart size={32} className="fill-foreground"/>RGY</span>
                    </Link>
                </NavbarBrand>

                <NavbarContent justify="start">
                    <NavbarItem isActive={pathname === '/me/projects'}>
                        <Link href={'/me/projects'}>
                            Мои проекты
                        </Link>
                    </NavbarItem>
                    <NavbarItem isActive={pathname === '/me/profile'}>
                        <Link
                            href={'/me/profile'}>
                            Профиль
                        </Link>
                    </NavbarItem>
                </NavbarContent>


                <NavbarContent
                    justify="end"
                    className="w-fit data-[justify=end]:flex-grow-0"
                >
                    <NotificationsDropdown/>

                    <div className="max-md:hidden">
                        <CircleHelp strokeWidth={2} className="text-default-400"/>
                    </div>


                    <NavbarContent>
                        <UserDropdown/>
                    </NavbarContent>
                </NavbarContent>
            </Navbar>
            {children}
        </div>
    );
};

import {
    Avatar,
    Dropdown,
    DropdownItem,
    DropdownMenu,
    DropdownTrigger,
    Navbar,
    NavbarItem, useDisclosure,
} from "@nextui-org/react";
import React from "react";
import {DarkModeSwitch} from "./darkmodeswitch";
import LogoutModal from "@/components/modals/LogoutModal";
import {useProfile} from "@/hooks/user.hooks";

export const UserDropdown = () => {
    const {data: profile} = useProfile()
    const {isOpen, onOpen, onOpenChange} = useDisclosure();
    if (!profile) return <></>
    return (
        <>
            <Dropdown>
                <NavbarItem>
                    <DropdownTrigger>
                        <Avatar
                            as="button"
                            color="secondary"
                            size="md"
                            src={profile.photo}
                        />
                    </DropdownTrigger>
                </NavbarItem>
                <DropdownMenu
                    aria-label="User menu actions"
                    onAction={(actionKey) => console.log({actionKey})}
                >
                    <DropdownItem
                        key="profile"
                        className="flex flex-col justify-start w-full items-start"
                    >
                        <p>Вы вошли как</p>
                        <p className='font-medium'>{profile.user.email}</p>
                    </DropdownItem>
                    {/*<DropdownItem key="settings">My Settings</DropdownItem>*/}
                    {/*<DropdownItem key="team_settings">Team Settings</DropdownItem>*/}
                    {/*<DropdownItem key="analytics">Analytics</DropdownItem>*/}
                    {/*<DropdownItem key="system">System</DropdownItem>*/}
                    {/*<DropdownItem key="configurations">Configurations</DropdownItem>*/}
                    {/*<DropdownItem key="help_and_feedback">Help & Feedback</DropdownItem>*/}
                    <DropdownItem key="logout" color="danger" className="text-danger " onClick={onOpen}>
                        Выйти
                    </DropdownItem>
                    <DropdownItem key="switch">
                        <DarkModeSwitch/>
                    </DropdownItem>
                </DropdownMenu>
            </Dropdown>

            <LogoutModal isOpen={isOpen} onOpenChange={onOpenChange}/>
        </>
    );
};

'use client'
import React from 'react';
import {Sidebar} from "@/components/sidebar/sidebar.styles";
import {RecentDropdown} from "@/components/sidebar/companies-dropdown";
import {SidebarItem} from "@/components/sidebar/sidebar-item";
import {HomeIcon} from "@/components/icons/sidebar/home-icon";
import {SidebarMenu} from "@/components/sidebar/sidebar-menu";
import {PaymentsIcon} from "@/components/icons/sidebar/payments-icon";
import {CustomersIcon} from "@/components/icons/sidebar/customers-icon";
import {SettingsIcon} from "@/components/icons/sidebar/settings-icon";
import {usePathname} from "next/navigation";
import {useSidebarContext} from "@/components/layout/layout-context";
import clsx from "clsx";
import {Folder, Group, Kanban, Settings, SquareKanban, User2, UserRoundPlus, Users, UsersRound} from "lucide-react";
import {PRIVATE_URLS} from "@/app/urlsConfig";
import {useProjectParams} from "@/app/me/projects/[projectId]/providers";

const Aside = () => {
    const pathname = usePathname();
    const projectId = useProjectParams()
    const {collapsed, setCollapsed} = useSidebarContext();
    return (
        <aside className="flex flex-col ">
            {/*{collapsed ? (<div className={Sidebar.Overlay()} onClick={setCollapsed}/>) : null}*/}

            <div className={clsx(Sidebar({collapsed: collapsed,}), 'flex flex-1 flex-col h-full overflow-hidden')}>
                <div className={Sidebar.Header()}>
                    <RecentDropdown/>
                </div>
                <div className="flex-1 overflow-y-auto">
                    <div className="flex flex-col justify-between  ">
                        <div className={clsx(Sidebar.Body(),)}>
                            <SidebarItem
                                title="Проект"
                                icon={<Folder/>}
                                isActive={pathname === PRIVATE_URLS.PROJECT(projectId)}
                                href={PRIVATE_URLS.PROJECT(projectId)}
                            />
                            <SidebarMenu title="Главное меню">
                                <SidebarItem
                                    title="Доска"
                                    icon={<SquareKanban/>}
                                    isActive={pathname === PRIVATE_URLS.BOARD(projectId)}
                                    href={PRIVATE_URLS.BOARD(projectId)}
                                />
                                <SidebarItem
                                    isActive={pathname === PRIVATE_URLS.MEMBERS(projectId)}
                                    title="Участники"
                                    icon={<UsersRound/>}
                                    href={PRIVATE_URLS.MEMBERS(projectId)}
                                />
                                <SidebarItem
                                    isActive={pathname === PRIVATE_URLS.GROUPS(projectId)}
                                    title="Группы"
                                    icon={<Group/>}
                                    href={PRIVATE_URLS.GROUPS(projectId)}
                                />
                                {/*<CollapseItems*/}
                                {/*    icon={<BalanceIcon/>}*/}
                                {/*    items={["Banks Accounts", "Credit Cards", "Loans"]}*/}
                                {/*    title="Balances"*/}
                                {/*/>*/}

                                {/*<SidebarItem*/}
                                {/*    isActive={pathname === "/products"}*/}
                                {/*    title="Products"*/}
                                {/*    icon={<ProductsIcon/>}*/}
                                {/*/>*/}
                                {/*<SidebarItem*/}
                                {/*    isActive={pathname === "/reports"}*/}
                                {/*    title="Reports"*/}
                                {/*    icon={<ReportsIcon/>}*/}
                                {/*/>*/}
                            </SidebarMenu>

                            <SidebarMenu title="Общее">
                                <SidebarItem
                                    isActive={pathname === "/settings"}
                                    title="Приглашения"
                                    icon={<UserRoundPlus/>}
                                />
                                <SidebarItem
                                    isActive={pathname === PRIVATE_URLS.PROJECT_SETTINGS(projectId)}
                                    title="Настройки"
                                    icon={<Settings/>}
                                />
                            </SidebarMenu>

                            {/*<SidebarMenu title="Updates">*/}
                            {/*    <SidebarItem*/}
                            {/*        isActive={pathname === "/changelog"}*/}
                            {/*        title="Changelog"*/}
                            {/*        icon={<ChangeLogIcon/>}*/}
                            {/*    />*/}
                            {/*</SidebarMenu>*/}
                        </div>
                        {/*<div className={Sidebar.Footer()}>*/}
                        {/*    <Tooltip content={"Settings"} color="primary">*/}
                        {/*        <div className="max-w-fit">*/}
                        {/*            <SettingsIcon/>*/}
                        {/*        </div>*/}
                        {/*    </Tooltip>*/}
                        {/*    <Tooltip content={"Adjustments"} color="primary">*/}
                        {/*        <div className="max-w-fit">*/}
                        {/*            <FilterIcon/>*/}
                        {/*        </div>*/}
                        {/*    </Tooltip>*/}
                        {/*    <Tooltip content={"Profile"} color="primary">*/}
                        {/*        <Avatar*/}
                        {/*            src="https://i.pravatar.cc/150?u=a042581f4e29026704d"*/}
                        {/*            size="sm"*/}
                        {/*        />*/}
                        {/*    </Tooltip>*/}
                        {/*</div>*/}
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Aside;
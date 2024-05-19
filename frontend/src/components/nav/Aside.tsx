import React from 'react';
import {Sidebar} from "@/components/sidebar/sidebar.styles";
import {CompaniesDropdown} from "@/components/sidebar/companies-dropdown";
import {SidebarItem} from "@/components/sidebar/sidebar-item";
import {HomeIcon} from "@/components/icons/sidebar/home-icon";
import {SidebarMenu} from "@/components/sidebar/sidebar-menu";
import {AccountsIcon} from "@/components/icons/sidebar/accounts-icon";
import {PaymentsIcon} from "@/components/icons/sidebar/payments-icon";
import {CollapseItems} from "@/components/sidebar/collapse-items";
import {BalanceIcon} from "@/components/icons/sidebar/balance-icon";
import {CustomersIcon} from "@/components/icons/sidebar/customers-icon";
import {ProductsIcon} from "@/components/icons/sidebar/products-icon";
import {ReportsIcon} from "@/components/icons/sidebar/reports-icon";
import {DevIcon} from "@/components/icons/sidebar/dev-icon";
import {ViewIcon} from "@/components/icons/sidebar/view-icon";
import {SettingsIcon} from "@/components/icons/sidebar/settings-icon";
import {ChangeLogIcon} from "@/components/icons/sidebar/changelog-icon";
import {Avatar, Tooltip} from "@nextui-org/react";
import {FilterIcon} from "@/components/icons/sidebar/filter-icon";
import {usePathname} from "next/navigation";
import {useSidebarContext} from "@/components/layout/layout-context";
import clsx from "clsx";

const Aside = () => {
    const pathname = usePathname();
    const {collapsed, setCollapsed} = useSidebarContext();
    return (
        <aside className="flex flex-col ">
            {collapsed ? (<div className={Sidebar.Overlay()} onClick={setCollapsed}/>) : null}

            <div className={clsx(Sidebar({collapsed: collapsed,}), 'flex flex-1 flex-col h-full overflow-hidden')}>
                <div className={Sidebar.Header()}>
                    <CompaniesDropdown/>
                </div>
                <div className="flex-1 overflow-y-auto">
                    <div className="flex flex-col justify-between  ">
                        <div className={clsx(Sidebar.Body(),)}>
                            <SidebarItem
                                title="Home"
                                icon={<HomeIcon/>}
                                isActive={pathname === "/"}
                                href="/"
                            />
                            <SidebarMenu title="Main Menu">
                                <SidebarItem
                                    isActive={pathname === "/accounts"}
                                    title="Доска"
                                    icon={<AccountsIcon/>}
                                    href="accounts"
                                />
                                <SidebarItem
                                    isActive={pathname === "/payments"}
                                    title="Payments"
                                    icon={<PaymentsIcon/>}
                                />
                                <CollapseItems
                                    icon={<BalanceIcon/>}
                                    items={["Banks Accounts", "Credit Cards", "Loans"]}
                                    title="Balances"
                                />
                                <SidebarItem
                                    isActive={pathname === "/customers"}
                                    title="Customers"
                                    icon={<CustomersIcon/>}
                                />
                                <SidebarItem
                                    isActive={pathname === "/products"}
                                    title="Products"
                                    icon={<ProductsIcon/>}
                                />
                                <SidebarItem
                                    isActive={pathname === "/reports"}
                                    title="Reports"
                                    icon={<ReportsIcon/>}
                                />
                            </SidebarMenu>

                            <SidebarMenu title="General">
                                <SidebarItem
                                    isActive={pathname === "/developers"}
                                    title="Developers"
                                    icon={<DevIcon/>}
                                />
                                <SidebarItem
                                    isActive={pathname === "/view"}
                                    title="View Test Data"
                                    icon={<ViewIcon/>}
                                />
                                <SidebarItem
                                    isActive={pathname === "/settings"}
                                    title="Settings"
                                    icon={<SettingsIcon/>}
                                />
                            </SidebarMenu>

                            <SidebarMenu title="Updates">
                                <SidebarItem
                                    isActive={pathname === "/changelog"}
                                    title="Changelog"
                                    icon={<ChangeLogIcon/>}
                                />
                            </SidebarMenu>
                        </div>
                        <div className={Sidebar.Footer()}>
                            <Tooltip content={"Settings"} color="primary">
                                <div className="max-w-fit">
                                    <SettingsIcon/>
                                </div>
                            </Tooltip>
                            <Tooltip content={"Adjustments"} color="primary">
                                <div className="max-w-fit">
                                    <FilterIcon/>
                                </div>
                            </Tooltip>
                            <Tooltip content={"Profile"} color="primary">
                                <Avatar
                                    src="https://i.pravatar.cc/150?u=a042581f4e29026704d"
                                    size="sm"
                                />
                            </Tooltip>
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Aside;
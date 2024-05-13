import React from "react";
import {useLockedBody} from "../hooks/useBodyLock";
import {NavbarWrapper} from "../navbar/navbar";
import {SidebarWrapper} from "../sidebar/sidebar";
import {SidebarContext} from "./layout-context";

interface Props {
    children: React.ReactNode;
}

export const Layout = ({children}: Props) => {
    const [sidebarOpen, setSidebarOpen] = React.useState(false);
    const [_, setLocked] = useLockedBody(false);
    const handleToggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
        setLocked(!sidebarOpen);
    };

    return (
        <SidebarContext.Provider
            value={{
                collapsed: sidebarOpen,
                setCollapsed: handleToggleSidebar,
            }}
        >
            <NavbarWrapper>
                <section className="flex overflow-y-hidden">
                    <SidebarWrapper/>

                    <div className="w-full overflow-y-scroll">
                        {children}
                    </div>
                </section>

            </NavbarWrapper>

        </SidebarContext.Provider>
    );
};

"use client";
import {
    Chip,
    Dropdown,
    DropdownItem,
    DropdownMenu,
    DropdownSection,
    DropdownTrigger,
} from "@nextui-org/react";
import React, {useEffect, useState} from "react";
import {AcmeIcon} from "../icons/acme-icon";
import {AcmeLogo} from "../icons/acmelogo";
import {BottomIcon} from "../icons/sidebar/bottom-icon";
import {getRecentProjects, IResentProject} from "@/app/me/projects/recent";
import {IProject} from "@/types/project.types";
import Link from "next/link";
import {ArrowDown, ChevronDown, Circle} from "lucide-react";
import {PRIVATE_URLS} from "@/app/urlsConfig";
import {useProjectParams} from "@/app/me/projects/[projectId]/providers";
import Image from "next/image";

export const RecentDropdown = () => {
    const projectId = useProjectParams()
    const [recentProjects, setRecentProjects] = useState<IResentProject[]>([]);
    const [current, setCurrent] = useState<IResentProject>()

    useEffect(() => {
        const recentProjects = getRecentProjects();
        setRecentProjects(recentProjects);

        if (!current && recentProjects.length > 0) {
            setCurrent(recentProjects[0]);
        }
    }, [current]);

    const formatDate = (dateString: string) => {
        const options: Intl.DateTimeFormatOptions = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    return (
        <Dropdown
            className={'flex-1'}
            classNames={{
                base: "w-full min-w-[260px]",
            }}
        >
            <DropdownTrigger className="flex-1 cursor-pointer">
                <div className="flex flex-1 items-center gap-2">
                    {current?.photo ?
                        <div className="relative object-cover w-10 h-10 rounded-md overflow-hidden">
                            <Image src={current.photo} alt={current.name} fill objectFit={'cover'}/>
                        </div>

                        : <AcmeIcon/>
                    }

                    <div className="flex flex-1 items-center">
                        <h3 className="m-0 overflow-hidden text-ellipsis whitespace-nowrap font-medium w-[125px] text-md text-default-900">
                            {current?.name}
                        </h3>
                        <ChevronDown size={16}/>
                        {/*<Chip*/}
                        {/*    startContent={<Circle strokeWidth={0} size={16} fill={current.color_hex}/>}*/}
                        {/*    variant="faded"*/}
                        {/*    className="text-foreground"*/}
                        {/*>*/}
                        {/*    {name}*/}
                        {/*</Chip>*/}
                        {/*<span*/}
                        {/*    className="text-xs font-light text-default-500">{current?.lastVisited ? formatDate(current.lastVisited) : ''}*/}
                        {/*</span>*/}
                    </div>

                </div>
            </DropdownTrigger>
            <DropdownMenu
                // onAction={(e) => {
                //     if (e === "1") {
                //         setCompany({
                //             name: "Facebook",
                //             location: "San Fransico, CA",
                //             logo: <AcmeIcon/>,
                //         });
                //     }
                //     if (e === "2") {
                //         setCompany({
                //             name: "Instagram",
                //             location: "Austin, Tx",
                //             logo: <AcmeLogo/>,
                //         });
                //     }
                //     if (e === "3") {
                //         setCompany({
                //             name: "Twitter",
                //             location: "Brooklyn, NY",
                //             logo: <AcmeIcon/>,
                //         });
                //     }
                //     if (e === "4") {
                //         setCompany({
                //             name: "Acme Co.",
                //             location: "Palo Alto, CA",
                //             logo: <AcmeIcon/>,
                //         });
                //     }
                // }}
                // aria-label="Avatar Actions"
            >
                <DropdownSection title="Недавние проекты">
                    {recentProjects.map((project, key) => {
                        return (
                            <DropdownItem
                                // as={Link}
                                // href={PRIVATE_URLS.PROJECT(project.id)}
                                key={key}
                                description={formatDate(project.lastVisited)}
                                startContent={
                                    current?.photo ?
                                        <div className="relative object-cover w-12 h-10 rounded-md overflow-hidden">
                                            <Image src={current.photo} alt={current.name} fill objectFit={'cover'}/>
                                        </div>
                                        : <AcmeIcon/>
                                }
                                classNames={{
                                    base: "py-4",
                                    title: "text-base font-semibold",
                                }}>
                                <Link href={PRIVATE_URLS.PROJECT(project.id)}>     {project.name}</Link>

                            </DropdownItem>)
                    })}
                </DropdownSection>
                <DropdownItem key="view-all">
                    <Link className='flex justify-center text-primary' href={PRIVATE_URLS.PROJECTS}>
                        Просмотреть все проекты
                    </Link>
                </DropdownItem>
            </DropdownMenu>
        </Dropdown>
    );
};
{/*<DropdownItem*/
}
{/*    key="1"*/
}
{/*    startContent={<AcmeIcon/>}*/
}
{/*    description="San Fransico, CA"*/
}
{/*    classNames={{*/
}
{/*        base: "py-4",*/
}
{/*        title: "text-base font-semibold",*/
}
{/*    }}*/
}
{/*>*/
}
{/*    Facebook*/
}
{/*</DropdownItem>*/
}
{/*<DropdownItem*/
}
{/*    key="2"*/
}
{/*    startContent={<AcmeLogo/>}*/
}
{/*    description="Austin, Tx"*/
}
{/*    classNames={{*/
}
{/*        base: "py-4",*/
}
{/*        title: "text-base font-semibold",*/
}
{/*    }}*/
}
{/*>*/
}
{/*    Instagram*/
}
{/*</DropdownItem>*/
}
{/*<DropdownItem*/
}
{/*    key="3"*/
}
{/*    startContent={<AcmeIcon/>}*/
}
{/*    description="Brooklyn, NY"*/
}
{/*    classNames={{*/
}
{/*        base: "py-4",*/
}
{/*        title: "text-base font-semibold",*/
}
{/*    }}*/
}
{/*>*/
}
{/*    Twitter*/
}
{/*</DropdownItem>*/
}
{/*<DropdownItem*/
}
{/*    key="4"*/
}
{/*    startContent={<AcmeIcon/>}*/
}
{/*    description="Palo Alto, CA"*/
}
{/*    classNames={{*/
}
{/*        base: "py-4",*/
}
{/*        title: "text-base font-semibold",*/
}
{/*    }}*/
}
{/*>*/
}
{/*    Acme Co.*/
}

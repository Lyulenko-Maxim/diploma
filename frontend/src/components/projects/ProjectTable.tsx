'use client'
import React from 'react';
import ProjectsList from "@/components/projects/ProjectsList";
import {SquarePlus} from "lucide-react";
import {Button} from '@nextui-org/react';


const ProjectTable = () => {
    const columns = [
        {key: "grip", label: "",},
        {key: "name", label: "НАЗВАНИЕ",},
        {key: "my_group", label: "МОЯ ГРУППА",},
        {key: "owner", label: "ВЛАДЕЛЕЦ",},
        {key: "members", label: "УЧАСТНИКИ",},
    ];

    return (
        <div className='flex-1'>
            <div className='grid w-full p-4 grid-cols-[.05fr_.3fr_.3fr_.3fr_.3fr_.3fr]'>
                {columns.map((column) =>
                    <div key={column.key}>{column.label}</div>
                )}
            </div>
            <Button radius='none' className='flex justify-center items-center w-full bg-foreground text-background'>
                <div className="grid grid-cols-[.03fr_.095fr_] items-center w-full">
                    <SquarePlus/>
                    <span>Создать новый проект</span>
                </div>
            </Button>
            <ProjectsList columns={columns}/>
        </div>
    );
};


export default ProjectTable;
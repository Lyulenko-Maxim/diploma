import React, {FC, Fragment} from 'react';
import {Draggable} from "@hello-pangea/dnd";
import {GripVertical} from "lucide-react";
import Link from "next/link";
import {IProjectItemProps} from "@/types/project.types";
import {renderCells} from "@/components/projects/renderCells";


const ProjectItem: FC<IProjectItemProps> = ({item, index, columns}) => {
    return (
        <Link href={`./projects/${item.id}`}>
            <Draggable index={index} draggableId={item.id}>
                {provided => (
                    <div key={item.id} ref={provided.innerRef}
                         {...provided.draggableProps}
                         className='grid w-full items-center rounded-sm border-opacity-40 p-4 border-b-1 border-foreground bg-background grid-cols-[.05fr_.3fr_.3fr_.3fr_.3fr_.3fr]'>

                        <div {...provided.dragHandleProps} className='hover:cursor-grab'>
                            <GripVertical/>
                        </div>

                        {columns.map((column, index) => {
                            if (index === 0) return null;
                            return (
                                <Fragment key={column.key}>
                                    {renderCells(item, column)}
                                </Fragment>
                            );
                        })}
                    </div>
                )}
            </Draggable>
        </Link>

    );
};

export default ProjectItem;
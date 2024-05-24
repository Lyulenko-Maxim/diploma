import React, {useCallback} from "react";
import {IMember} from "@/types/project.types";
import {Button, Chip, getKeyValue, Tooltip, User} from "@nextui-org/react";
import {Circle, UserX2} from "lucide-react";
import {IGroup} from "@/types/group.types";

export const useRenderGroupsTable = () => {
    const renderCell = useCallback((group: IGroup, columnId: string) => {
        switch (columnId) {
            case "groups":
                return (
                    <Chip
                        startContent={<Circle strokeWidth={0} size={16} fill={group.color_hex}/>}
                        variant="flat"
                        radius='sm'
                        className="text-foreground">
                        <p className="text-sm capitalize text-bold">{group.name}</p>
                    </Chip>
                );
            case "members":
                return (
                    <>{group.color_hex}</>
                );

            case "actions":
                return (
                    <div className="relative flex items-center gap-2">
                        <Tooltip color="danger" content="Исключить">
                            <Button isIconOnly className={'bg-transparent'}>
                                <UserX2 className='text-danger'/>
                            </Button>

                        </Tooltip>
                    </div>
                );
            default:
                return null;
        }
    }, []);

    return {renderCell}
}

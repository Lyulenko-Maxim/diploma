import React, {FC, useEffect, useRef, useState, KeyboardEvent} from 'react';
import {Button, Card, CardBody, Kbd, Textarea} from "@nextui-org/react";
import clsx from "clsx";
import {CardFooter} from "@nextui-org/card";
import {SquarePlus} from "lucide-react";
import {useTaskCreate} from "@/hooks/task.hooks";
import {IStatus} from "@/types/status.types";
import {useProjectParams} from "@/app/me/projects/[projectId]/providers";

export interface CreateTaskItemProps {
    status: IStatus
}

const CreateTaskItem: FC<CreateTaskItemProps> = ({status}) => {
    const projectId = useProjectParams()
    const [isExpanded, setIsExpanded] = useState<boolean>(false);
    const [value, setValue] = React.useState("");
    const cardRef = useRef<HTMLDivElement | null>(null);
    const textareaRef = useRef<HTMLTextAreaElement | null>(null);

    const handleCardClick = () => {
        setIsExpanded(true);
        setTimeout(() => {
            textareaRef.current?.focus();
        }, 0);
    };
    const {mutate, isSuccess, isPending} = useTaskCreate()

    const handleKeyDown = (event: KeyboardEvent) => {
        if (event.key === 'Enter') {
            handleCreateTask()
        }
    };

    const handleCreateTask = () => {
        if (value.trim() != '')
            mutate({projectId: projectId, data: {title: value, status: status.id}})
    }

    const handleClickOutside = (event: MouseEvent) => {
        if (cardRef.current && !cardRef.current.contains(event.target as Node)) {
            setIsExpanded(false);
        }
    };

    useEffect(() => {
        if (isSuccess && !isPending) {
            setIsExpanded(false)
            setTimeout(() => {
                setValue('')
            }, 1)

        }
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isSuccess, isPending]);

    return (
        <>
            <Card ref={cardRef}
                  radius='sm'
                  className={clsx("bg-content1 mb-2 w-[350px] ml-[17.5px]", {
                      'hidden': !isExpanded,
                      'block': isExpanded
                  })}>
                <CardBody>
                    <Textarea
                        ref={textareaRef}
                        maxLength={32}
                        variant="underlined"
                        placeholder="Что нужно сделать?"
                        value={value}
                        maxRows={1}
                        onValueChange={setValue}
                        onKeyDown={handleKeyDown}
                    />
                </CardBody>
                <CardFooter className='flex items-center justify-end'>
                    <Button onPress={handleCreateTask}
                            onKeyDown={handleKeyDown}
                            isLoading={isPending}
                            isDisabled={value.trim() == '' || isPending}
                            className=""
                            radius="sm"
                            variant='solid'
                            size="sm">
                        Добавить
                        <Kbd className='bg-transparent shadow-none' keys={["enter"]}/>
                    </Button>
                </CardFooter>
            </Card>
            <Button onPress={handleCardClick}
                    radius='sm'

                    className={clsx('flex w-[350px] mx-[17.5px] gap-4 bg-content1 pl-3 py-6 mb-2 shadow-medium justify-start',
                        {'hidden': isExpanded,}
                    )}>
                <SquarePlus className='text-foreground'/>
                Добавить задачу
            </Button>
        </>
    );
};

export default CreateTaskItem;
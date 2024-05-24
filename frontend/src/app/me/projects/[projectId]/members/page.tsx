'use client'
import React, {useEffect, useMemo, useState} from 'react';
import {
    Table,
    TableHeader,
    TableColumn,
    TableBody,
    TableRow,
    TableCell,
    Image,
    User,
    Chip,
    Tooltip,
    getKeyValue,
    ModalContent,
    ModalHeader,
    Modal,
    ModalBody,
    ModalFooter,
    Button,
    useDisclosure,
    Card,
    CardBody,
    Popover, PopoverTrigger, PopoverContent, ListboxItem, Listbox
} from "@nextui-org/react";
import {IMember, IMemberDetails} from "@/types/project.types";
import {useMemberCurrent, useMemberList, useMemberRetrieve} from "@/hooks/members.hooks";
import {usePathname, useRouter, useSearchParams} from 'next/navigation';
import {Circle, DeleteIcon, EditIcon, Plus, UserMinus, UserX, UserX2} from "lucide-react";
import NextImage from "next/image";
import {Divider} from "@nextui-org/divider";
import {useGroupList} from "@/hooks/group.hooks";

const columns = [
    {name: "УЧАСТНИК", uid: "username"},
    {name: "ГРУППА", uid: "highest_group"},
    {name: "В ЧИСЛЕ УЧАСТНИКОВ С", uid: "created_at"},
    {name: "ДЕЙСТВИЯ", uid: "actions"},
];


const Page = () => {
    const formatDate = (date: Date) => {
        const dateString = date
        const options: Intl.DateTimeFormatOptions = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };
    const renderCell = React.useCallback((member: IMember, columnId: string) => {
        const cellValue = getKeyValue(member, columnId);

        switch (columnId) {
            case "username":
                return (
                    <User
                        onClick={() => onMemberClick(member.id)}
                        className={'bg-transparent cursor-pointer'}
                        avatarProps={{radius: "full", src: member.profile.photo}}
                        description={(member.profile.first_name + ' ' || '') + (member.profile.last_name || '')}
                        name={member.profile.username}
                    />
                );
            case "highest_group":
                return (
                    <Chip
                        startContent={<Circle strokeWidth={0} size={16} fill={member.highest_group.color_hex}/>}
                        variant="faded"
                        className="text-foreground">
                        <p className="text-sm capitalize text-bold">{member.highest_group.name}</p>
                    </Chip>
                );
            case "created_at":
                return (
                    <p className="text-sm capitalize text-bold">
                        {member.created_at ? formatDate((member.created_at)) : ''}
                    </p>
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
                return cellValue;
        }
    }, []);

    const pathname = usePathname()
    const projectId = pathname.split('/').slice(-2, -1)[0]
    const {items: members, setItems: setMembers} = useMemberList(projectId)
    const {isOpen, onOpen, onOpenChange} = useDisclosure();
    const [memberId, setMemberId] = useState<string>('')
    const {data} = useMemberRetrieve(projectId, memberId)
    const {items: groups, setItems: setGroups} = useGroupList(projectId)
    const {data: currentMember} = useMemberCurrent(projectId)
    const onMemberClick = (id: string) => {
        setMemberId(id)
        onOpen()
    }

    const availableGroups = useMemo(() => {
        if (!data || !groups || !currentMember) return [];

        const memberGroupIds = new Set(data.groups.map(group => group.id));

        const currentMemberMaxOrder = currentMember.highest_group.order

        return groups.filter(group =>
            !memberGroupIds.has(group.id) && (currentMember.is_owner || group.order >= currentMemberMaxOrder)
        );
    }, [data, groups, currentMember]);

    if (!members) {
        return <div></div>
    }
    return (
        <>
            <Modal isOpen={isOpen} onOpenChange={onOpenChange} radius='sm'>
                <ModalContent>
                    {(onClose) => (
                        <>
                            <ModalHeader style={{backgroundColor: data?.profile.banner_color_hex}}
                                         className="relative mb-12 flex h-16 flex-col gap-1">
                                <Image
                                    as={NextImage}
                                    width={200}
                                    height={200}
                                    src={data?.profile.photo}
                                    radius='full'
                                    className="relative h-24 w-24 border-5 border-content1 object-cover text-xl transition ease-in-out hover:cursor-pointer"
                                    alt="Avatar"/>

                            </ModalHeader>
                            <ModalBody>
                                <Card radius='sm' className='py-2' shadow={'sm'}>
                                    <CardBody className='flex flex-col gap-4'>
                                        <div className='flex flex-col gap-2'>
                                            <h1 className='text-lg font-medium'>{data?.profile.username}</h1>
                                            <h1 className='text-sm'>{(data?.profile.first_name + ' ' || '') + (data?.profile.last_name || '')}</h1>
                                        </div>
                                        <Divider/>
                                        <div className='flex flex-col gap-2'>
                                            <h1 className='text-small font-medium'>В ЧИСЛЕ УЧАСТНИКОВ С</h1>
                                            <p className='text-small font-normal'>{data?.created_at ? formatDate(data?.created_at) : ''}</p>
                                        </div>

                                        <div className='flex flex-col gap-2'>
                                            <h1 className='text-small font-medium'>ГРУППЫ</h1>
                                            <div className='flex flex-wrap items-center'>

                                                {data?.groups.map(group => {
                                                    return (
                                                        <Chip key={group.id}
                                                              radius={'sm'}
                                                              variant={'flat'}
                                                              className="text-foreground mr-2 mb-2"
                                                              onClose={() => console.log("close")}
                                                              startContent={
                                                                  <Circle strokeWidth={0} size={16}
                                                                          fill={group.color_hex}
                                                                  />
                                                              }>
                                                            <p className="text-sm capitalize text-bold">{group.name}</p>
                                                        </Chip>
                                                    )
                                                })}

                                                <Popover radius={'sm'} showArrow placement="bottom">
                                                    <PopoverTrigger>
                                                        <Chip as={Button}
                                                              variant="flat"
                                                              radius='sm'
                                                              className="text-foreground mb-2">
                                                            <Plus size={16} className=''/>
                                                        </Chip>
                                                    </PopoverTrigger>
                                                    <PopoverContent>
                                                        <div
                                                            className="w-full max-w-[260px] px-1 py-2 border-default-200 dark:border-default-100">
                                                            <Listbox
                                                                topContent={<h1 className={'mb-4'}>Доступные
                                                                    группы</h1>}
                                                                items={availableGroups}
                                                                aria-label="Dynamic Actions"
                                                                classNames={{
                                                                    list: "max-h-[100px] overflow-y-scroll",
                                                                }}
                                                                onAction={(key) => alert(key)}
                                                            >
                                                                {(group) => (
                                                                    <ListboxItem key={group.id}>
                                                                        <div className='flex items-center gap-2'>
                                                                            <Circle strokeWidth={0} size={16}
                                                                                    fill={group.color_hex}
                                                                            />
                                                                            <p className="text-sm capitalize text-bold">{group.name}</p>
                                                                        </div>
                                                                    </ListboxItem>
                                                                )}
                                                            </Listbox>

                                                        </div>
                                                    </PopoverContent>
                                                </Popover>

                                            </div>

                                        </div>


                                    </CardBody>
                                </Card>
                            </ModalBody>
                            <ModalFooter>
                                {/*<Button color="danger" variant="light" onPress={onClose}>*/}
                                {/*    Close*/}
                                {/*</Button>*/}
                                {/*<Button color="primary" onPress={onClose}>*/}
                                {/*    Action*/}
                                {/*</Button>*/}
                            </ModalFooter>
                        </>
                    )}
                </ModalContent>
            </Modal>
            <Table radius={'none'}>
                <TableHeader columns={columns}>
                    {(column) => (
                        <TableColumn key={column.uid} align={column.uid === "actions" ? "center" : "start"}>
                            {column.name}
                        </TableColumn>
                    )}
                </TableHeader>
                <TableBody>
                    {members.map((member) => (

                        <TableRow key={member.id}>
                            {columns.map((column) => (
                                <TableCell key={column.uid}>{renderCell(member, column.uid)}</TableCell>
                            ))}
                        </TableRow>
                    ))}

                </TableBody>
            </Table>
        </>
    );
};

export default Page;